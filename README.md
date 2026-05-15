# YouCloned skills registry

A live registry of skill instructions fetched at runtime by the YouCloned bootstrap plugin for Claude Cowork.

## Structure

- `manifest.json` — index of available skills (name, URL, description)
- `skills/*.md` — individual skill instruction files

## How it works

A small Cowork plugin installed locally on each user's machine has one router skill. When triggered, it fetches `manifest.json` from this repo, picks the matching skill, fetches that skill's markdown, and follows the instructions inside.

Updates here propagate to every user on their next conversation — no plugin reinstall required.
