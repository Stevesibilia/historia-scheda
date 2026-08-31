# Historia — Scheda del Personaggio

A Python script that generates a print-ready A4 PDF character sheet for the **Historia** tabletop RPG system.

## Features

The generated character sheet includes:

- **Header** — character name, family, species, and profession; initiative, inspiration, speed, PP, and fortune fields
- **Abilità (Skills)** — all 18 skills with proficiency marker, competence checkbox, modifier box, and attribute reference
- **Caratteristiche (Ability Scores)** — six stats (Forza, Intelligenza, Destrezza, Saggezza, Costituzione, Carisma) in a 2×3 grid with modifier sub-boxes
- **Competenze (Proficiencies)** — free-text proficiency block with a Bonus inset box
- **Personality** — Tratto, Ideale, Legame, Difetto side-by-side boxes
- **Combat** — Classe Armatura (with Indebolimento tracker), Attacchi table (4 rows), Azioni / Azioni Bonus / Reazioni
- **P. Ferita & Dadi Vita** — current/max HP and hit-dice tracking
- **Conio (Currency)** — MO, MA, MR, ME, MB coin slots
- **Equipaggiamento** — free-text equipment list

The visual style uses a warm parchment palette with decorative borders, banner labels, and corner ornaments.

## Fillable form

The PDF is a fillable AcroForm: every input has a text field or checkbox on top of
the printed decoration, so the sheet can be filled in a PDF viewer or left blank and
filled by hand. Field names are stable, accent-free ids (`nome`, `stat_for`,
`mod_for`, `cpt_atletica`, `mst_atletica`, `skmod_atletica`, `attacco1_danno`,
`conio_mo`, `dado_vita_7`, …), so the sheet can also be filled programmatically.

Ruled areas (Competenze, Tratto/Ideale/Legame/Difetto, Azioni, Equipaggiamento) have
one field per printed rule, numbered from the top down — `competenze_1`,
`pers_tratto_1`, `azioni_1`, `equipaggiamento_1`, … Equipaggiamento numbers run down
the left column and continue in the right one.

## Requirements

- Python 3.8+
- [just](https://github.com/casey/just) (optional but recommended)

## Usage

### With just (recommended)

```bash
just          # generate the PDF (creates venv and installs deps automatically on first run)
just open     # generate and open in the default viewer
just setup    # explicit venv creation + install + generate
```

The venv is created automatically the first time you run `just generate` or `just open` — no manual setup needed.

### Without just

```bash
python3 -m venv .venv
.venv/bin/pip install reportlab
.venv/bin/python scheda_v3.py
```

## Output

The PDF is written to `output/scheda_personaggio_v{VERSION}.pdf`. The `output/` directory is created automatically. The version is defined by the `VERSION` constant at the top of `scheda_v3.py`.

Pre-built PDFs are attached to each [GitHub release](https://github.com/Stevesibilia/historia-scheda/releases).

## License

MIT
