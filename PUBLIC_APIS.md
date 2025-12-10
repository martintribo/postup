# Public API & Component Reference

This document enumerates every callable server function, route action, and reusable component that is meant to be consumed by the rest of the codebase (or external clients) in this repository. Each section lists accepted inputs, side effects, and concrete usage examples so you can plug these pieces into new features without re-reading the entire source tree.

> **Tip:** File paths in headings point to the owning source so you can jump back to the implementation quickly.

---

## Environment & Secrets

| Variable | Required | Used by | Notes |
| --- | --- | --- | --- |
| `DATABASE_URL` | ✅ | `src/lib/server/db/index.ts` | Neon/Drizzle connection string; process will crash on startup if unset. |
| `PUBLIC_MAPBOX_ACCESS_TOKEN` or `MAPBOX_ACCESS_TOKEN` | ✅ (either) | `LocationAutocomplete`, reverse geocoder | Public version can be embedded in the client; private one (preferred) lives on the server. |

Mapbox requests fail fast when no token is configured, so set one in `.env` and redeploy.

---

## Request Lifecycle (`src/hooks.server.ts`)

The `handle` hook wraps every request to attach authentication context:

1. Reads the `auth-session` cookie.
2. If missing, generates an anonymous session via `auth.getOrCreateAnonymousSession(event)` and stores the resulting hash in `event.locals.anonymousSessionId`.
3. If present, validates the session with `auth.validateSessionToken(token)`:
   - Valid sessions are renewed (if needed) and expose `event.locals.user`, `event.locals.session`, and set `anonymousSessionId` to the real session ID.
   - Invalid sessions are deleted and replaced with a fresh anonymous session/cookie pair.

Downstream load functions and actions can rely on:

```ts
interface Locals {
  user: SessionValidationResult['user'];
  session: SessionValidationResult['session'];
  anonymousSessionId: string; // always defined
}
```

---

## Server Modules

### `$lib/server/auth.ts`

| Export | Description | Example |
| --- | --- | --- |
| `generateSessionToken()` | Returns a random base64url token (18 bytes entropy). | `const token = auth.generateSessionToken();` |
| `createSession(token, userId)` | Hashes the token (SHA-256) and inserts a `session` row that expires in 30 days. Returns the inserted session. | `const session = await auth.createSession(token, user.id);` |
| `validateSessionToken(token)` | Looks up the hashed token, renews it when <15 days remain, and returns `{ session, user }`. Deletes expired sessions. | `const { user } = await auth.validateSessionToken(token);` |
| `invalidateSession(id)` | Deletes the session row; use when logging out. | `await auth.invalidateSession(session.id);` |
| `setSessionTokenCookie(event, token, expiresAt)` | Sets the HTTP-only `auth-session` cookie on `/`. | `auth.setSessionTokenCookie(event, token, session.expiresAt);` |
| `deleteSessionTokenCookie(event)` | Removes `auth-session`. | `auth.deleteSessionTokenCookie(event);` |
| `generateAnonymousSessionToken()` / `getAnonymousSessionId(token)` | Utility pair for stateless anonymous session cookies. |  |
| `getOrCreateAnonymousSession(event)` | Returns the hashed ID for the anonymous session, creating and setting a cookie (1-year expiry) if needed. | `const anonSession = auth.getOrCreateAnonymousSession(event);` |
| `getAnonymousSessionIdFromCookie(event)` | Reads and hashes the anonymous cookie when you only need the ID (read-only). |  |

#### Usage Pattern

```ts
import * as auth from '$lib/server/auth';

const token = auth.generateSessionToken();
const session = await auth.createSession(token, user.id);
auth.setSessionTokenCookie(event, token, session.expiresAt);
```

This is exactly how the `/demo/lucia/login` action provisions sessions.

---

### `$lib/server/db/schema.ts`

| Table | Columns | Notes |
| --- | --- | --- |
| `user` | `id` (text PK), `username` (unique), `passwordHash`, `age?` | `username` is enforced unique and validated in the login route. |
| `session` | `id` (text PK), `userId` FK → `user.id`, `expiresAt` (timestamp with TZ) | `id` is the SHA-256 hash of the cookie token. |
| `post` | `id` (serial PK), `name`, `activity`, `location`, `latitude`, `longitude`, `hours`, `neighborhood?`, `locality?`, `district?`, `sessionId?`, `createdAt`, `startTime` | Posts belong to an (anonymous or authenticated) session via `sessionId`. `startTime` defaults to `now`. |

`export type Session`, `User`, and `Post` are inferred so you can import strong types anywhere in the app.

---

### `$lib/server/db/index.ts`

Exports a configured Drizzle client:

```ts
import { db } from '$lib/server/db';
const posts = await db.select().from(post);
```

The module throws during import if `DATABASE_URL` is missing, which surfaces configuration issues at startup rather than at first query.

---

## Root Feed Routes (`src/routes/+page.server.ts`)

### `load(event)`

1. Retrieves (or creates) `event.locals.anonymousSessionId` from the handle hook.
2. Determines the client’s location via `getClientAddress()`:
   - `127.0.0.1`/`localhost` short-circuit to Los Angeles for developer convenience.
   - Otherwise, queries `http://ip-api.com/json/{ip}` and falls back to London on failure.
3. Fetches active posts within 200 miles using a Drizzle/Haversine SQL expression.
4. Returns `{ location, posts, anonymousSessionId, form }`, where `form` is a Superform instance bound to the Zod `postSchema`.

**Client-side usage:** the root page imports the data via `let { data } = $props()` and wires it into the `Map` and sidebar list.

### `actions.delete`

- **Input:** `FormData` containing `postId` (string).
- **Guards:** Ensures the post exists and that `post.sessionId === event.locals.anonymousSessionId`.
- **Side effects:** Deletes the row and streams updated `posts` back to the client so the UI refreshes.
- **Errors:** `400` for malformed IDs, `403` when session mismatch, `404` when missing, `500` on DB failures.

#### Example (fetch API)

```ts
await fetch('?/delete', {
  method: 'POST',
  body: new URLSearchParams({ postId: String(post.id) })
});
```

### `actions.create`

- **Input:** Superform-enhanced request body matching `postSchema` (name, activity, location text, numeric latitude/longitude, hours 1–24).
- **Process:**
  1. Validates via `superValidate`.
  2. Reverse-geocodes the coordinates with Mapbox v6 to enrich the post with `neighborhood`, `locality`, and `district`.
  3. Associates the row with `event.locals.anonymousSessionId` (either logged-in session or anonymous hash).
  4. Returns a fresh `form` object plus the refreshed feed on success; fails with status `400`/`500` and includes `posts` so the UI can stay in sync.

#### Example (Svelte form enhancement)

```svelte
<form method="POST" action="?/create" use:enhance>
  <!-- bind `name`, `activity`, `location`, hidden lat/lon, `hours` -->
</form>
```

You can also hit the endpoint from outside the app:

```bash
curl -X POST 'https://your.app/?/create' \
  -H 'Content-Type: application/json' \
  -d '{
        "name":"Alex",
        "activity":"Pair programming",
        "location":"Verve Coffee, LA",
        "latitude":34.0901,
        "longitude":-118.3617,
        "hours":3
      }'
```

(Include the `anon-session` cookie so ownership checks work later.)

---

## Demo Authentication Routes (`src/routes/demo/lucia/*`)

These files demonstrate Lucia-style auth flows backed by the same `auth` helpers.

### `GET /demo/lucia/login`

Redirects to `/demo/lucia` if already authenticated. Otherwise renders a simple username/password form (`src/routes/demo/lucia/login/+page.svelte`).

### `POST /demo/lucia/login`

- Parses `username` and `password`.
- Validates using `validateUsername` (3–31 chars, `a-z0-9_-`) and `validatePassword` (6–255 chars).
- Looks up the user via Drizzle, verifies the Argon2 hash, and provisions a new session token/cookie pair via `auth.createSession` and `auth.setSessionTokenCookie`.
- Redirects to `/demo/lucia` on success or returns `400` with `form.message` on failure.

### `POST /demo/lucia/register`

- Validates the inputs, generates a base32 user ID, hashes the password with Argon2, inserts the row, and logs the user in automatically (same session provisioning snippet as login).

### `GET /demo/lucia`

- Uses `requireLogin()` (server-only helper calling `getRequestEvent()`) to redirect anonymous visitors.
- Returns `{ user }` for display in `+page.svelte`.

### `POST /demo/lucia?/logout`

- Requires `event.locals.session`.
- Calls `auth.invalidateSession` and clears the cookie before redirecting back to the login form.

Use these routes as blueprints when extending authentication deeper into the main app.

---

## UI Components

### `Map` (`src/lib/components/Map.svelte`)

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `latitude` | `number` | — | Center latitude for the viewport. |
| `longitude` | `number` | — | Center longitude. |
| `city` / `country` | `string?` | — | Optional metadata you can surface elsewhere. |
| `posts` | `Post[]` | `[]` | Each post renders a custom Leaflet marker with popup content. |

Key behaviors:

- Loads Leaflet lazily on mount, disables native attribution UI, and fits the map to a 40×40 mile bounding box via `calculateBounds()`.
- Watches `posts` reactively and re-renders markers whenever the array changes.
- Automatically switches between light (OpenStreetMap) and dark (CartoDB Dark Matter) tile layers based on `prefers-color-scheme` and updates tiles on-the-fly when the preference flips.
- Keeps the map responsive using both `window.resize` and `ResizeObserver`.

#### Usage Example

```svelte
<Map
  latitude={data.location.latitude}
  longitude={data.location.longitude}
  posts={data.posts}
/>
```

When providing your own posts, make sure they satisfy `Post` (import from `$lib/server/db/schema`).

---

### `LocationAutocomplete` (`src/lib/components/LocationAutocomplete.svelte`)

| Prop | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | ✅ | Text input `name` attribute so native forms pick up the value. |
| `value` | `string` | ✅ (bindable) | Initial text value; use `$bindable('')` from the parent to sync with Superform. |
| `onSelect` | `(location) => void` | ✅ | Receives `{ name, latitude, longitude }` from the chosen suggestion. Use it to set hidden form fields. |
| `proximity` | `{ latitude: number; longitude: number }` | ⛔️ | Optional hint so Mapbox can rank nearby places first. |

Behavior highlights:

- Debounces user input (300 ms) before calling the Mapbox Search v6 forward geocoder.
- Handles v6 response nuances (`properties.coordinates`, `geometry.coordinates`, or legacy `center`).
- Keyboard-accessible suggestion list with arrow navigation, Enter to select, and Escape to collapse.
- Automatically hides the suggestion list on blur (with a short delay so click events register).

#### Usage Example

```svelte
<LocationAutocomplete
  name="location"
  bind:value={locationValue}
  proximity={{ latitude: data.location.latitude, longitude: data.location.longitude }}
  onSelect={({ name, latitude, longitude }) => {
    locationValue = name;
    $form.location = name;
    $form.latitude = latitude;
    $form.longitude = longitude;
  }}
/>
```

Remember to include hidden `<input>` fields (as the root page does) so form submissions carry the numeric coordinates.

---

### Storybook Components (`src/stories/*`)

These follow the default SvelteKit + Storybook template but are still reusable.

- `Button.svelte`: Simple CTA with `primary`, `backgroundColor`, `size`, and `label` props. Accepts any native button attribute via rest props.
  ```svelte
  <Button primary size="large" label="Invite" onclick={() => console.log('clicked')} />
  ```
- `Header.svelte`: Composes the `Button` component to show login/logout states. Pass a `user` object to show the welcome banner, or pass `onLogin`/`onLogout` callbacks to wire up events.
- `Page.svelte`: Demonstrates how to manage shared state (`user`) and pass handlers into `Header`. Useful as a layout stub when building marketing pages in Storybook.

---

## Root Page UI Helpers (`src/routes/+page.svelte`)

While these functions are not exported, they illustrate how to combine the public APIs:

- `handleLocationSelect` demonstrates the correct `onSelect` plumbing for `LocationAutocomplete`.
- `incrementHours` / `decrementHours` enforce the 1–24 hour bounds defined in the Zod schema.
- Modal helpers (`openFormModal`, `closeFormModal`) show how to layer the UI on top of the map.

Use this file as a canonical reference implementation when building new pages around the same primitives.

---

## Example Flow: Creating & Managing a Post

1. **Client acquires coordinates** via `LocationAutocomplete` and binds them into the Superform state.
2. **User submits the modal form** (`?/create`):
   ```svelte
   <form method="POST" action="?/create" use:enhance>
     <input name="name" bind:value={$form.name} />
     <!-- ...other fields... -->
   </form>
   ```
3. **Server action** validates, reverse-geocodes, stores the post, and ties it to the anonymous session.
4. **Map & sidebar** re-render automatically with the new `posts` array returned by the action.
5. **Deletion** later sends `postId` to `?/delete`, which cross-checks the stored `sessionId` against `event.locals.anonymousSessionId` to prevent tampering.

With the pieces above you can replicate the same end-to-end flow on additional routes or even expose a mobile client simply by reusing the same endpoints and cookies.
