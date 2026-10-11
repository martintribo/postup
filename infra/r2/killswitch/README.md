# PostUp R2 spend kill switch

Disables public `r2.dev` access on bucket `postup-tiles` when Class B reads
(GetObject / HeadObject / …) exceed:

- month-to-date default **50,000,000** (~$14.40 over the 10M free tier)
- any UTC hour default **5,000,000**

Runs every 5 minutes via a systemd **user** timer on dev-vm.

## Token

Uses `~/.config/postup/cloudflare.env` (`CLOUDFLARE_API_TOKEN`,
`CLOUDFLARE_ACCOUNT_ID`). No secrets in git.

Required permissions on `postup-terraform-r2`:

| Permission | Why |
|---|---|
| Account → Workers R2 Storage → Edit (and Read) | GET/PUT `/r2/buckets/postup-tiles/domains/managed` |
| User → API Tokens → Edit | Terraform rclone token (already on the bootstrap token) |
| **Account → Account Analytics → Read** | GraphQL `r2OperationsAdaptiveGroups` |

If Analytics Read is missing, the checker logs `ANALYTICS_UNAUTHORIZED` and
will not disable the domain (it cannot see spend). Add that permission on the
existing token; do not create a wider one.

## Install

```bash
bash infra/r2/killswitch/install.sh
```

Config copy: `~/.config/postup/killswitch.env` (from `killswitch.env.example`).
Thresholds are env vars there.

## Commands

```bash
python3 infra/r2/killswitch/killswitch.py status     # r2.dev on/off
python3 infra/r2/killswitch/killswitch.py dry-run    # query only
python3 infra/r2/killswitch/killswitch.py check      # query; disable if over
python3 infra/r2/killswitch/killswitch.py disable    # force off (test / manual)
python3 infra/r2/killswitch/killswitch.py enable     # re-enable public r2.dev
```

## Re-enable (manual)

After a trip, public access stays off until a person runs:

```bash
python3 /home/main/.agenthub/worktrees/postup/postup-protomaps/infra/r2/killswitch/killswitch.py enable
```

Terraform `cloudflare_r2_managed_domain.tiles` has `enabled = true`. A later
`terraform apply` would also turn r2.dev back on (state drift after a trip).
Prefer the `enable` command so apply is not required.

Do not set CORS `AllowedOrigins` to `*`.

## Logs

```bash
journalctl --user -u postup-r2-killswitch.service -n 80 --no-pager
systemctl --user list-timers | grep postup-r2
```

State (mode 600): `~/.config/postup/killswitch/state.json`

On a trip, the checker POSTs `http://127.0.0.1:3051/bus/send` to Chief of Staff
(`BUS_TO`) with the Class B counts.
