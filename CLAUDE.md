# pabloKM/ISLANAUT — instructions for Claude

This repo is the home for **every game PabloKM and Claude make together**. Whenever a
session builds or changes a game, push it here without being asked. That is the standing
agreement with Pablo.

## Adding or updating a game

1. One folder per game: `games/<slug>/` (kebab-case, e.g. `crowd-crossing`).
   - `index.html` — the playable game. One self-contained file is the norm. Extra assets
     (music, textures, models) go next to it and are loaded with relative paths.
   - `game.json` — metadata for the front page:
     ```json
     {
       "title": "Crowd Crossing",
       "blurb": "Frogger inside out: gather strays, hold hands, cross together.",
       "date": "2026-11-01",
       "updated": "2026-11-06",
       "tags": ["mobile", "arcade"],
       "controls": "Drag to move, tap to grab hands",
       "artifact": "https://claude.ai/artifact/..."
     }
     ```
     Bump `updated` on every change, because the front page sorts by it.
   - `thumb.png` or `thumb.jpg` (optional, about 16:10) is the card image. Without one, a
     coloured letter tile is shown.
2. Don't edit the root `index.html` by hand. `scripts/build-index.mjs` builds it from the
   `game.json` files. Run `node scripts/build-index.mjs` locally to preview it.
3. Commit with a message like `crowd-crossing: add hand-holding chain` and push to `main`.
   The Pages workflow deploys within about a minute to
   `https://pablokm.github.io/ISLANAUT/games/<slug>/`.
4. If the game is also a claude.ai artifact, keep the two in sync and put the artifact link
   in `game.json`.

## Notes
- Exclude Sid Dash. It isn't Pablo's work.
- Large binaries: keep single files under about 50 MB. Prefer compressed audio (ogg/mp3).
- Games that already have their own repo (e.g. `pabloKM/Tuto`, `pabloKM/TiTaTo-`) can
  still get a folder here, either as a copy or as a small redirect page to their own
  Pages site.
