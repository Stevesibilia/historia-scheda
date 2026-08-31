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
| `tfield` | Transparent AcroForm text field laid over drawn decoration |
| `cbox` | Invisible AcroForm checkbox laid over a drawn frame |
| `dot` | Small tickable circle: drawn frame + circular checkbox |
| `slug` | Accent-stripped snake_case name used for form field ids |

Layout is coordinate-based (ReportLab canvas). The page is A4 (`W, H = A4`). Margin is `M = 16` pt. Columns are hand-computed as `LX/CX/RX` with widths `LW/CW/RW`.

## Form Fields

The sheet is fillable: every decoration is still drawn by hand, and a transparent
AcroForm widget is laid on top of it. Rules:

- Text fields go through `tfield` (or `iline(..., field="name")`, which places one
  above the rule, after the label). Pass `q=Q_CENTRE` for numeric boxes.
- Ruled free-text areas get one field per rule, not a single multiline field, so
  typed text lands on the printed lines: number them `<area>_1`, `<area>_2`, …
  from the top rule down (Equipaggiamento numbers straight through column 1 and
  on into column 2).
- Checkboxes go through `cbox` / `dot`. Never use reportlab's `shape='circle'`
  checkbox: it mis-scales its own frame for any `size` other than 20 pt. Draw the
  circle with `c.circle` and overlay `cbox(..., style='circle')` instead.
- Do not set `NeedAppearances` on the AcroForm. It makes viewers discard the
  reportlab appearance streams and redraw every checkbox as a plain square.
- Field names are stable, lowercase, accent-free ids (`stat_for`, `cpt_atletica`,
  `skmod_atletica`, `attacco1_danno`, `conio_mo`, …). Treat them as an API:
  external tools fill the sheet by name, so rename only when necessary.

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

**Add a fillable input**: draw the decoration first, then overlay the widget with `tfield`, `cbox` or `dot` — never rely on the widget to draw its own border.

**Change text**: skill names are in the `skills` list; stat names are in `stats`; coin codes/names are in `coins`; personality box names are in `pers_names`.
