output "bucket_name" {
  value = cloudflare_r2_bucket.tiles.name
}

output "r2_dev_domain" {
  description = "Host for the managed r2.dev URL (no scheme)."
  value       = cloudflare_r2_managed_domain.tiles.domain
}

output "tiles_url" {
  description = "PUBLIC_TILES_URL for the worktree after the planet object is uploaded."
  value       = "https://${cloudflare_r2_managed_domain.tiles.domain}/basemap.pmtiles"
}

output "cors_rule_count" {
  value = length(local.cors_rules)
}

output "cors_origin_count" {
  value = 1 + length(local.worktree_origins)
}

# S3 API: Access Key ID is the token id; Secret is SHA-256 of the token value.
# https://developers.cloudflare.com/r2/api/tokens/
output "rclone_s3_access_key_id" {
  value     = cloudflare_api_token.rclone.id
  sensitive = true
}

output "rclone_s3_secret_access_key" {
  value     = sha256(cloudflare_api_token.rclone.value)
  sensitive = true
}

output "rclone_s3_endpoint" {
  value = "https://${var.account_id}.r2.cloudflarestorage.com"
}
