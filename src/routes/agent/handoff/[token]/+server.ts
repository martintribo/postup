import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { validateAgentToken } from '$lib/server/auth';

export const GET: RequestHandler = async ({ params, url, request }) => {
	const token = params.token;
	const agent = await validateAgentToken(token);
	if (!agent) {
		throw error(401, 'Token is invalid, expired, or revoked.');
	}

	const wantsJson = (request.headers.get('accept') ?? '').includes('application/json');
	const base = url.origin;

	const body =
		agent.scope === 'status'
			? wantsJson
				? statusJson(token, base)
				: statusMarkdown(token, base)
			: wantsJson
				? projectsJson(token, base)
				: projectsMarkdown(token, base);

	return new Response(body, {
		headers: {
			'content-type': wantsJson ? 'application/json' : 'text/markdown; charset=utf-8'
		}
	});
};

function projectsJson(token: string, base: string): string {
	return JSON.stringify(
		{
			scope: 'projects',
			token,
			expiresIn: '1 hour from issuance',
			authHeader: `Authorization: Bearer ${token}`,
			note: 'All writes are staged for human review. They are not visible to anyone else until the user accepts them.',
			writingGuidance: {
				name: 'Recognizable, ≤ 50 chars. No tagline padding.',
				shortDescription:
					'One sentence (≤ 100 chars). A stranger should know what this is at a glance.',
				description:
					'2-4 short paragraphs. Lead with what it is and why it is interesting; cut everything else.',
				imagePlaceholders:
					'In `description`, insert markdown image tags with `placeholder` as the URL where a picture would help: ![alt describing the shot](placeholder). The user clicks each placeholder later to upload the real image. Suggest 1-3 placeholders per project, only where a picture genuinely aids comprehension. Make the alt text specific — it tells the user what to upload.'
			},
			endpoints: [
				{
					method: 'GET',
					url: `${base}/api/agent/projects`,
					description: "List the user's projects, plus your own pending staged changes."
				},
				{
					method: 'POST',
					url: `${base}/api/agent/projects`,
					description:
						'Propose a new project. Body: { name, type?, shortDescription?, description? }. type ∈ software|art|writing|business|activities (default software).'
				},
				{
					method: 'PATCH',
					url: `${base}/api/agent/projects/{id}`,
					description:
						'Propose an update to a project owned by the user. Body may include: name, type, shortDescription, description, active.'
				}
			]
		},
		null,
		2
	);
}

function projectsMarkdown(token: string, base: string): string {
	return `# Agent handoff — projects

You have been given a temporary access token by a logged-in user of postup so you can propose changes to their projects on their behalf.

## How to authenticate

Send this header on every request:

\`\`\`
Authorization: Bearer ${token}
\`\`\`

The token is valid for **1 hour** from issuance and can be revoked at any time.

## Important: changes are staged

**Nothing you do is applied immediately.** Every create or update is recorded as a "pending change" that the user will review and accept or reject. Do not assume your edits are live.

## Writing guidance

**Be succinct.** Project listings are scanned, not read.

- **\`name\`** — recognizable, ≤ 50 chars, no tagline padding.
- **\`shortDescription\`** — one sentence (≤ 100 chars). A stranger should know what this is at a glance.
- **\`description\`** — 2-4 short paragraphs. Lead with what it is and why it is interesting; cut everything else.

**Suggest image placeholders.** Project pages should be visual. In \`description\`, insert markdown image tags with \`placeholder\` as the URL where a picture would help. The user will click each placeholder later to upload the real image.

    ![screenshot of the dashboard](placeholder)
    ![the team during a hackathon](placeholder)

Suggest 1-3 placeholders per project, only where a picture genuinely aids comprehension. The alt text is what tells the user (and you, later) what kind of picture belongs there — make it specific.

## Endpoints

### List projects and your pending changes
\`\`\`
GET ${base}/api/agent/projects
\`\`\`
Returns \`{ projects: [...], pendingChanges: [...] }\`. Use this to see what already exists before proposing edits.

### Propose a new project
\`\`\`
POST ${base}/api/agent/projects
Content-Type: application/json

{
  "name": "string (required, ≤ 50 chars)",
  "type": "software | art | writing | business | activities (default: software)",
  "shortDescription": "string (≤ 100 chars)",
  "description": "string with markdown; include 1-3 ![alt](placeholder) tags"
}
\`\`\`

### Propose an update to an existing project
\`\`\`
PATCH ${base}/api/agent/projects/{id}
Content-Type: application/json

{
  "name": "string (optional)",
  "type": "string (optional)",
  "shortDescription": "string (optional)",
  "description": "string (optional)",
  "active": "boolean (optional)"
}
\`\`\`
Only fields present in the body are proposed; omitted fields are unchanged. The project must belong to the user who issued the token.

## What to do next

1. \`GET /api/agent/projects\` to see what the user already has.
2. Propose your changes via POST/PATCH.
3. Tell the user to review pending changes in their projects page.
`;
}

function statusJson(token: string, base: string): string {
	return JSON.stringify(
		{
			scope: 'status',
			token,
			expiresIn: '1 hour from issuance',
			authHeader: `Authorization: Bearer ${token}`,
			note: 'Status entries are staged for review. The user accepts or rejects each one.',
			writingGuidance: {
				audience:
					'A human reader, casually browsing the project. Not the user who built it — somebody who wants to see what the project is up to.',
				aggregation:
					'Group related work into one entry per work session (or per coherent chunk). Do NOT emit one entry per commit. If git is available, cluster commits by time (≥ 2 hour gap = new session) and topic. If git is not available, ask the user where one chunk ends and the next begins; if neither is possible, write one entry per several days of work rather than per item.',
				shape:
					'Each entry has a short title (a headline, like "Shipped agent handoff" or "Made the map responsive") and a body of 2-5 short paragraphs. The body should explain WHAT was built, WHY it matters, and at least one INTERESTING implementation detail (a tricky bit, a tradeoff, a surprise). Tone is curious and concrete, not corporate.',
				context:
					'Before writing, look for context: README, design docs, the diff itself, code comments, related issues, commit messages. Name the actual files/components/concepts the work touched. A good entry teaches the reader something about the project.',
				dates:
					'occurredAt is required. Use the date the work landed (last commit in the cluster, or merge time). Use lastStatusAt from GET /api/agent/projects as your lower bound — never write entries older than that.',
				length:
					'Aim for 150-400 words per body. Under 80 words is almost certainly under-aggregated. Over 600 words means it should be split.'
			},
			endpoints: [
				{
					method: 'GET',
					url: `${base}/api/agent/projects`,
					description:
						"List the user's projects and your own pending changes. Each project may include lastStatusAt — use it as the lower bound for new entries."
				},
				{
					method: 'POST',
					url: `${base}/api/agent/projects/{id}/status`,
					description:
						'Propose a status update. Body: { title?, body, occurredAt (ISO 8601) }. title is a short headline; body is 2-5 paragraphs.'
				}
			]
		},
		null,
		2
	);
}

function statusMarkdown(token: string, base: string): string {
	return `# Agent handoff — status updates

You have been given a temporary access token by a logged-in user of postup so you can post status updates on their projects on their behalf.

## How to authenticate

Send this header on every request:

\`\`\`
Authorization: Bearer ${token}
\`\`\`

The token is valid for **1 hour** and is scoped to status updates only — you cannot create or edit projects with it.

## Important: entries are staged

Every status update is staged. The user reviews and accepts or rejects each one before it appears.

## Who you are writing for

A human, casually browsing the project page — *not* the person who built it. Someone who wants to know what this project has been up to recently and would enjoy a little story about it.

## Aggregate by work session

**Do not emit one entry per commit.** One commit is too small to be worth a human's time. Cluster related work and emit one entry per coherent chunk:

- **If git is available:** group commits by time and topic. A ≥ 2-hour gap between commits, or a clear topic shift (auth → UI → infra), is usually a new session. A single session may be 1 commit or 30; what matters is whether they tell one story.
- **If git is not available:** ask the user where the chunks are, or bias to fewer/bigger entries (one per few days of work) rather than micro-blogs.

Use \`lastStatusAt\` (from \`GET /api/agent/projects\`) as the lower bound — don't write entries older than the last accepted one.

## Shape of an entry

Each entry has a **short title** (a headline) and a **body of 2-5 short paragraphs**. The body should answer:

1. **What** was built or changed?
2. **Why** does it matter — what does the project gain?
3. **One interesting implementation detail** — a tradeoff, a surprise, a tricky bit, a "huh, didn't expect that" moment.

Tone is curious and concrete, like a developer writing a small blog post. Not corporate. Not bullet lists. Don't say "implemented feature X" — say what feature X *does* and what it was like to build.

### Length

Aim for **150-400 words per body**. Under 80 words is almost certainly under-aggregated (you're emitting per-commit). Over 600 means split it into two entries.

## Get context before you write

Don't write blind from \`git log\` alone. Look at:

- The README, AGENTS.md, or any design docs in the repo.
- The actual diff for the relevant commits — what files changed, what functions appeared.
- Code comments and commit message bodies.
- Any linked issues or PR descriptions.

Name the actual files, components, or concepts in the body (e.g. "the new \`handleAuth\` hook in \`src/hooks.server.ts\`"). A good entry teaches the reader something they couldn't have guessed from the project description.

## Example

\`\`\`
{
  "title": "Agent handoff for project edits",
  "body": "Added a way for a logged-in user to hand off API access to an AI agent. Click an 'Agent handoff' button, get a URL, paste it into your agent of choice — the agent fetches the URL, reads instructions, and starts proposing changes.\\n\\nThe interesting bit: changes are not applied directly. Everything an agent does lands in a project_change table with status='pending'. The owner reviews a diff-style preview and accepts or rejects each one. This means a token leak is mostly harmless — the attacker can spam proposals but cannot actually edit anything.\\n\\nThe handoff URL itself returns markdown when fetched, so the agent reads it the same way a human would. Tokens are 1-hour, sha256-hashed at rest, and scoped (a 'status' token cannot edit projects). The scope ended up being the cleanest way to ship two different agent prompts from one mint endpoint.",
  "occurredAt": "2026-05-11T18:00:00Z"
}
\`\`\`

Notice: it names actual concepts (project_change table, handoff URL, scope), explains *why* (leak resistance, two prompts from one endpoint), and admits to a real implementation choice. That's the bar.

## Endpoints

### See projects and last status timestamps
\`\`\`
GET ${base}/api/agent/projects
\`\`\`
Each project may include \`lastStatusAt\` — your lower bound for new entries on that project.

### Propose a status update
\`\`\`
POST ${base}/api/agent/projects/{id}/status
Content-Type: application/json

{
  "title": "Short headline (optional but strongly preferred)",
  "body": "2-5 paragraphs. Plain text with \\\\n\\\\n between paragraphs. No markdown headings.",
  "occurredAt": "2026-05-09T18:00:00Z"
}
\`\`\`
The project must belong to the user who issued the token.

## What to do next

1. \`GET /api/agent/projects\` to see projects and last status timestamps.
2. For each project, gather context (git log + diffs + docs).
3. Cluster the work into sessions.
4. POST one entry per session, oldest first.
5. Tell the user to review pending entries on their projects page.
`;
}
