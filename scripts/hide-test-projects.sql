-- Run once after `drizzle-kit push` adds project.hidden (Martin/owner only, on prod after merge).
UPDATE project SET hidden = true
WHERE name IN ('E2E Project', 'Blogpost Test', 'Round-trip project');
