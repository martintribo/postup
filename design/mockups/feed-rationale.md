# Quiet state, feed-first: design rationale (mockup, Oct 14 2026)

## Why a feed can beat an empty map
An empty map tells people nothing is happening here. A feed of recent postups, even from earlier this week, says real people come here to work on cool things. What makes it appealing:
- **People first.** A face or avatar plus a first name. People join people, not pins.
- **What they're building.** "Star Fox 64 mod, new level" is the hook. Projects make a postup interesting and give a reason to say hi.
- **Real vibe photos.** The table, the laptop, the latte, the window light. This is what makes someone want to go.
- **Recency and proximity.** "2h ago · 0.4 mi" makes it feel alive and reachable.
- **Light social proof.** "3 postups here this week" and "2 joined" are small but honest. No inflated counts.
- **A low-effort ask.** One big "Post up" button, plus "Post up here" on each card. The map stays one tap away.

## Images
| Source | Can we use it in the feed? | Notes |
|---|---|---|
| **User photos** (taken at post-up time) | **Yes, the main one** | They're our own content, so we can store and reuse them. Over time they replace Google photos for each cafe (Martin's goal). Needs moderation and a report option. Strip EXIF/GPS. Default to framing the table, not faces. |
| **Project screenshots/images** (projects-agent already supports image upload) | Yes | Great for "what they're building" cards. |
| **Avatars** (Google/Apple profile picture after sign-in, or an initial) | Yes | Initial-in-a-color circle as the fallback. |
| **Google Places photos (UI Kit)** | **No, not in the feed** | They're only allowed inside Google's own UI Kit widget, with attribution, and can't be stored or reused. They stay on the cafe detail screen. |
| **Map snippet** (Stadia tile around our own coordinates) | Yes, as a fallback | Shows "where" with no photo. Needs the Stadia/OSM attribution. |

**Fallback when there's no image:** a warm gradient tinted per project with its initial or emoji, or a small map snippet. Never leave a grey box. Variant B (text-only) tests whether photos really matter.

## What posting should ask for
- Keep the three core fields (cafe, what you're working on, until when).
- Add **one optional "Add a photo of your spot" tile**: camera-first, skippable, never required.
- Ask for the photo **after** the postup is live on the confirmation screen ("Add a photo so people know the vibe"). That way it doesn't slow down posting.
- When a project is tagged, offer its latest screenshot as the card image.

## Recommendation
Make the quiet state feed-first with photos (variant A) when nothing is live nearby, with the map one tap away. Switch to map-first as soon as anything is live. Seed the feed with Martin's own postup photos and project screenshots. Variant B shows how it looks before photos exist.
