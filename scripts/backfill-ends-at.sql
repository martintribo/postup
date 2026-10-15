-- M3: run once after drizzle push on any DB with existing posts.
UPDATE post SET ends_at = start_time + (hours || ' hours')::interval WHERE ends_at IS NULL;
