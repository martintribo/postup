# PostUp mockups: source of truth

These mockups are the source of truth for the app on `phase/final`.

- Open `index.html` in a browser. It works from any static server, or straight from disk.
- Every screen must match its mockup in the **Fresh** style at **phone 390×844** and **desktop 1440×900**.
- Before you implement a screen, read `notes/<screen>.md`. `notes/all.md` has every screen plus the global rules. `llms.txt` is the index for LLMs.
- Scenarios are set with URL params: `?auth=out|in&live=live|none&mode=live|building` (mode applies to Home, `#home`, only). Other params: `style=fresh`, `device=phone|desktop`, `notes=0` (hides the notes panel and menu, for clean screenshots). Pick a screen with `#<screen-id>`, e.g. `index.html?device=phone&auth=in&live=none#home`.
- Note tags such as [F###], [FS], [R#] and [M1018*] point to sources (listed at the end of each note file). [unsourced] marks a line with no source; confirm it with Martin.

## Rebuild

`python3 gen/build.py`, run from this folder. Edit `gen/notes.md` for notes and `gen/*.py|css|js` for the screens. Don't hand-edit `index.html`, `notes/` or `llms.txt`; they are generated.

`shots/` holds older reference captures. `index.html` wins wherever they differ.
