Stage all changes, create a commit, and push to the remote.

> **A Jon Benson skill** · AI Collective: [collective.bnsn.ai](https://collective.bnsn.ai)

The vault has a `.git/hooks/pre-commit` that BLOCKS commits containing credential patterns. This command runs a pre-flight scrub so the hook stays silent: fix problems before they reach the hook, not after.

## Steps

### 0. Pre-flight credential scrub (before staging)

Scan the working tree (modified + untracked files) for hardcoded credentials. Patterns to detect:

- AWS access keys: `AKIA[0-9A-Z]{16}`
- OpenAI keys: `sk-(proj-)?[A-Za-z0-9_\-]{20,}`
- Anthropic keys: `sk-ant-[A-Za-z0-9_\-]{20,}`
- ElevenLabs keys: `sk_[a-f0-9]{40,}`
- GitHub PATs: `gh[ps]_[A-Za-z0-9]{36,}`
- JWT tokens: `eyJ[A-Za-z0-9_\-]{8,}\.eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}`
- Hardcoded password/api_key/token literals: `(?i)\b(password|passwd|api[_\-]?key|secret|token)\s*[:=]\s*['"][^'"\s]{12,}['"]`

Skip lines marked `# noqa: secret` or `pragma: allowlist secret`. Skip comment lines. Skip files inside `node_modules/`, `.git/`, `.env*`.

For each credential found:
1. Pick a clear env var name (e.g. `BNSN_SFTP_PASS`, `MAILVIO_API_KEY`).
2. If the value is not already in your project's `.env` (gitignored), append it: `KEY=value`.
3. Replace the literal in the source file:
   - Python: `os.environ["KEY"]`
   - Node/JS: `process.env.KEY`
   - Bash: `"$KEY"` (assumes the script sources .env first)
4. If the file does not already load `.env` at startup, add a loader near the top:
   - Python: small `_vault_env()` function that reads vault `.env` into `os.environ`
   - Node `.mjs`: IIFE that reads vault `.env` into `process.env`
5. Verify `import os` (Python) is present.

Surface the list of scrubbed files to the user before committing. Wait for confirmation if more than 5 files were modified.

### 1. Status + diff

- `git status` to see all changes
- `git diff --staged` and `git diff` to review

### 2. Stage

`git add` specific files (NOT `-A` blindly: avoid committing .env, .env.*, large binaries unless asked).

### 3. Commit

Concise message describing what + why. Pass via heredoc. Footer:

```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

If the pre-commit hook still blocks (your scan missed something), READ THE HOOK OUTPUT carefully, scrub the surfaced item, and retry. Do NOT bypass with `--no-verify` unless Jon explicitly says so.

### 4. Push

`git push` to current branch's remote. The user typing `/COM` is push approval. (For non-`/COM` commits, push needs separate explicit approval per Jon's `[Never Push Without Approval]` rule.)

### 5. Confirm

Show commit hash + branch state.

## Defense in depth

Three layers protect against credential leaks:

1. **This command (Step 0):** proactive scrub before staging
2. **`.git/hooks/pre-commit`:** blocks any commit (manual, this command, or auto-push) that still contains a credential pattern
3. **`scripts/auto-push.sh` + launchd:** nightly auto-backup that respects the hook (commit fails if creds present)
