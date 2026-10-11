# R2 CORS cannot wildcard ports (docs: list each origin; at most one * and it
# cannot sit in the port). 15000-15999 is 1000 host:port origins. No published
# per-rule origin cap; we chunk 100 origins per rule (S3-style) plus postup.now.

locals {
  worktree_origins = [
    for p in range(15000, 16000) : "https://dev-vm.burbot-fence.ts.net:${p}"
  ]

  cors_chunk = 100

  cors_rules = concat(
    [
      {
        id = "postup-now"
        allowed = {
          methods = ["GET", "HEAD"]
          origins = ["https://postup.now"]
          headers = ["range", "if-match"]
        }
        expose_headers  = ["etag", "ETag"]
        max_age_seconds = 3600
      }
    ],
    [
      for i in range(0, length(local.worktree_origins) / local.cors_chunk) : {
        id = "dev-vm-${15000 + i * local.cors_chunk}-${15000 + i * local.cors_chunk + local.cors_chunk - 1}"
        allowed = {
          methods = ["GET", "HEAD"]
          origins = slice(local.worktree_origins, i * local.cors_chunk, i * local.cors_chunk + local.cors_chunk)
          headers = ["range", "if-match"]
        }
        expose_headers  = ["etag", "ETag"]
        max_age_seconds = 3600
      }
    ]
  )
}

data "cloudflare_api_token_permission_groups_list" "all" {}

locals {
  r2_item_perms = {
    for x in data.cloudflare_api_token_permission_groups_list.all.result :
    x.name => x.id
    if contains([
      "Workers R2 Storage Bucket Item Read",
      "Workers R2 Storage Bucket Item Write",
    ], x.name)
  }
}

resource "cloudflare_r2_bucket" "tiles" {
  account_id = var.account_id
  name       = var.bucket_name
}

resource "cloudflare_r2_bucket_cors" "tiles" {
  account_id  = var.account_id
  bucket_name = cloudflare_r2_bucket.tiles.name
  rules       = local.cors_rules
}

resource "cloudflare_r2_managed_domain" "tiles" {
  account_id  = var.account_id
  bucket_name = cloudflare_r2_bucket.tiles.name
  enabled     = true
}

resource "cloudflare_api_token" "rclone" {
  name = "postup-tiles-rclone"
  policies = [{
    effect = "allow"
    permission_groups = [
      { id = local.r2_item_perms["Workers R2 Storage Bucket Item Read"] },
      { id = local.r2_item_perms["Workers R2 Storage Bucket Item Write"] },
    ]
    resources = jsonencode({
      "com.cloudflare.edge.r2.bucket.${var.account_id}_default_${cloudflare_r2_bucket.tiles.name}" = "*"
    })
  }]
}
