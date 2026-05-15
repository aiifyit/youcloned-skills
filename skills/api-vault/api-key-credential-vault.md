---
name: api-vault
description: "Credential security — intercept, store, and manage API keys, passwords, and tokens. Fires immediately whenever any credential appears in chat; highest priority after security-scanner."
---

# API Vault — Secure Credential Management

API keys and secrets must NEVER exist in chat logs, conversation history, or any file that isn't the protected `.env` file. This skill ensures that.

## Detection Rules

Monitor EVERY user message for patterns that look like credentials:
- Strings starting with `sk-`, `pk-`, `key_`, `token_`, `bearer `
- Long alphanumeric strings (32+ characters) that aren't normal words or URLs
- Anything the user explicitly calls a "key", "secret", "token", or "password"
- Strings matching common API key formats: `xxx-xxxx-xxxx-xxxx`, base64-encoded blobs

## If a Credential is Detected in Chat

1. **DO NOT acknowledge or repeat the key.** Do not echo it back, even partially.
2. Immediately tell the user: "I detected what looks like an API key in your message. For your security, I've flagged this — keys should never be pasted in chat. Let me open the secure key entry for you instead."
3. If you have the ability to purge the message from logs, do so.
4. Invoke the secure key entry flow below.

## Secure Key Entry Flow

### For Hosted Instances (DigitalOcean / Cloud Server)

1. Generate a temporary Cloudflare tunnel pointing to the `.env` file location on the server:
   ```bash
   # Start a lightweight HTTP server that serves ONLY the key entry form
   # on a random port, then tunnel it through Cloudflare
   python3 /tools/api-vault/serve_key_entry.py --env-path /home/openclaw/.env --mode hosted
   ```
2. The script will:
   - Start a minimal HTML form on a random local port
   - Launch a Cloudflare tunnel (`cloudflared tunnel --url http://localhost:<port>`)
   - Return the temporary public URL
3. Share the URL with the user: "Here's your secure key entry page: [URL]. This link expires in 10 minutes. Paste your keys there — they'll go directly into your configuration file."
4. The form accepts:
   - `ANTHROPIC_API_KEY` — Claude / Anthropic API key
   - `OPENAI_API_KEY` — OpenAI API key (optional)
   - `BENSON_API_KEY` — Benson copywriting API key (optional)
   - `STRIPE_SECRET_KEY` — Stripe secret key (optional)
   - `SMTP_PASSWORD` — Email SMTP password (optional)
   - Custom key name + value (for any other service)
5. On form submission:
   - Write each key to the `.env` file using proper `KEY=value` format
   - Append to existing `.env` without overwriting unrelated keys
   - Set file permissions to `600` (owner read/write only)
   - Kill the HTTP server and close the tunnel
   - Return confirmation to the agent

### For Local Instances (Mac Mini / Local Machine)

1. Generate a local HTML file and open it in the default browser:
   ```bash
   python3 /tools/api-vault/serve_key_entry.py --env-path /home/openclaw/.env --mode local
   ```
2. The script will:
   - Generate a self-contained HTML file at `/tmp/api-vault-entry.html`
   - The HTML form captures keys client-side and writes them via a local endpoint
   - Open the file in the default browser using `open` (macOS) or `xdg-open` (Linux)
3. Tell the user: "I've opened a secure key entry page in your browser. Paste your keys there — they'll be saved directly to your local configuration."
4. Same form fields as hosted version
5. On submission:
   - JavaScript POSTs to a localhost endpoint
   - The local server writes to `.env` and shuts down
   - Returns confirmation

## Key Rotation

When the user asks to change or rotate a key:

1. Ask which key they want to update
2. Launch the secure entry flow (hosted or local depending on environment)
3. The form pre-populates with key NAMES only (never values)
4. New values overwrite the old ones in `.env`
5. Confirm the update: "Your [KEY_NAME] has been updated. I'll use the new one going forward."

## Post-Onboarding Key Swap

During initial setup, the system ships with a temporary Anthropic API key funded by us. After onboarding, this skill is invoked to swap that temporary key for the user's own key. The flow:

1. Tell the user: "Your agent is currently running on a starter API key. To keep it running, you'll need to add your own Anthropic API key. I'll walk you through getting one if you don't have one yet."
2. If they don't have a key, guide them:
   - Go to console.anthropic.com
   - Create an account or sign in
   - Go to API Keys
   - Create a new key
   - Set up billing with auto-recharge (recommend $20 minimum with $10 auto-recharge to start)
3. Launch the secure key entry flow to capture their key
4. Verify the key works by making a minimal test API call
5. Confirm: "Your API key is active and working. You're all set — your agent is now running on your own account."

## Security Rules — Non-Negotiable

- NEVER store keys in any file other than `.env`
- NEVER echo, repeat, log, or display key values in chat
- NEVER include keys in any skill output, report, or document
- ALWAYS use the tunnel/browser flow for key entry
- ALWAYS set `.env` file permissions to 600
- ALWAYS kill the tunnel/server after key entry is complete
- If the secure entry infrastructure fails, tell the user to manually edit their `.env` file via SSH/terminal and provide the key names they need to add — but NEVER accept keys through chat as a fallback
