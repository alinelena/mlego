# newsite — Modern mlego Site

A modern, responsive showcase and documentation site for **mlego**, styled to match [alin.elena.re](https://alin.elena.re) (from `git@github.com:alinelena/eu.git`).

## Features

- **Exact Design Match with alin.elena.re**:
  - Dark background (`#0f1318` & `#161c24`) with glowing cyan (`#57cbcc`) and green (`#6cb670`) accents.
  - Floating corner navigation menu with avatar logo, animated hamburger bars, section label, and glassmorphism panel.
  - Parallax hero banner with interactive pulse badge, handwritten title accents (`Caveat`, `Kalam`), and social pill badges.
  - Parallax textured stone and brick background bands between sections.
  - Glassmorphic surface cards with hover elevation and glowing borders.
- **Full Content Preservation**:
  - All original Markdown documentation in `notes/` remains completely untouched.
  - Interactive **Document Reader Modal** renders full markdown documents on demand with `marked.js`, including tables, code blocks with copy buttons, and image zoom.
  - Direct URL hash routing (`#doc/m65`, `#doc/assembly`, etc.) allows deep linking to any article.
- **Hardware Showcase & Comparison**:
  - Categorized grids for Designed Keyboards (m66, m65, m60, m60 Split, m48, m20, m8, m4), Converted POS Terminals (Tipro 8×16, 8×12, 8×4, ANSI-Ortho, Ortho-ANSI), Liberated Mice (SteelSeries Prime), and Hardware Guides.
  - Real-time search and category filtering.
  - Side-by-side hardware comparison specification matrix.
- **Zero-Dependency & Offline Ready**:
  - Pre-bundled data in `assets/js/content-data.js` allows browsing locally via `file://` or any static HTTP server with zero CORS restrictions.

## Local Preview

To preview locally using Python:

```bash
# From workspace root:
python3 -m http.server 8080 --directory newsite
# Open http://localhost:8080 in your browser
```

## Rebuilding Data from notes/

If new markdown notes or edits are added to `notes/`, rebuild the newsite data bundle with:

```bash
uv run python3 tools/build_newsite.py
```

