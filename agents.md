# Historia Scheda — Agent Instructions

## Project Overview

Single-file Python script (`scheda_v3.py`) that generates an A4 PDF character sheet for the **Historia** tabletop RPG using `reportlab`. There are no other source files, no tests, and no configuration beyond the script itself.

## Architecture

Everything lives in `build()`. Helper functions are pure drawing utilities:

| Function | Role |
|---|---|
| `fancy_box` | Rounded box with drop-shadow and optional banner title |
| `banner` | Pill-shaped label with decorative ear triangles |
| `iline` | Single input line with optional small label |
| `diam_line` | Horizontal rule with a diamond ornament in the centre |
| `stat_block` | Square stat box with inner frame and modifier sub-box |
| `skill_row` | One skill row: proficiency circle, competence checkbox, mod box, name, attribute |
| `corner` | Corner ornament drawn at the four page margins |

Layout is coordinate-based (ReportLab canvas). The page is A4 (`W, H = A4`). Margin is `M = 16` pt. Columns are hand-computed as `LX/CX/RX` with widths `LW/CW/RW`.

## Colour Palette

All colours are defined as module-level constants. Never inline hex strings; always reference a named constant.

| Constant | Use |
|---|---|
| `INK` | Body text |
| `PARCHMENT` | Page background |
| `PARCHMENT_DK` | Stat/modifier box fill |
| `BORDER` | Box outlines, banner background |
| `ACCENT` | Labels, decorative elements |
| `LIGHT_LINE` | Input lines, inner frames |
| `FILL_BG` | Box interior fill |

## Output Path

Hardcoded in `build()`:

```python
c = canvas.Canvas("/mnt/user-data/outputs/scheda_personaggio.pdf", pagesize=A4)
```

When the user wants a different output path, change that string directly — there is no config file.

## What to Avoid

- Do not add command-line argument parsing unless explicitly requested; the script is intentionally simple.
- Do not split into multiple files or add a package structure.
- Do not add dependencies beyond `reportlab`.
- Do not generate test fixtures or sample PDFs committed to the repo.

## Common Tasks

**Add a new section**: follow the pattern of an existing section — compute `y` relative to the section above, call `diam_line` as a separator, then draw boxes with `fancy_box` and fill with `iline` rows.

**Adjust spacing**: all vertical positions are derived from `body_top`, `sk_y`, `pers_y`, `combat_top`, `bot_top`. Change the gap constants (`pers_h`, `combat_h`, etc.) to resize sections.

**Change text**: skill names are in the `skills` list; stat names are in `stats`; coin codes/names are in `coins`; personality box names are in `pers_names`.
