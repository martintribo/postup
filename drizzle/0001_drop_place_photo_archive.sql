-- Drop stored Google photo references and personal archive columns.
-- Place photos now come only from Places UI Kit widgets (loaded by google_place_id).
ALTER TABLE "place" DROP COLUMN IF EXISTS "photo_ref";
ALTER TABLE "place" DROP COLUMN IF EXISTS "photo_archived_at";
ALTER TABLE "place" DROP COLUMN IF EXISTS "photo_archive_key";
ALTER TABLE "place" DROP COLUMN IF EXISTS "photo_etag";
