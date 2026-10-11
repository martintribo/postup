terraform {
  required_version = ">= 1.5.0"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.27"
    }
  }

  # State lives on dev-vm, outside git. Do not put state in the public tiles bucket.
  backend "local" {
    path = "/home/main/.config/postup/terraform/postup-tiles/terraform.tfstate"
  }
}

provider "cloudflare" {
  # CLOUDFLARE_API_TOKEN from the environment (sourced from ~/.config/postup/cloudflare.env).
}

variable "account_id" {
  type        = string
  description = "Martin's Cloudflare account ID (TF_VAR_account_id / CLOUDFLARE_ACCOUNT_ID)."
}

variable "bucket_name" {
  type    = string
  default = "postup-tiles"
}
