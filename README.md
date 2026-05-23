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

## Requirements

- Python 3.8+
- [reportlab](https://pypi.org/project/reportlab/)

```bash
pip install reportlab
```

## Usage

```bash
python scheda_v3.py
```

The PDF is written to `/mnt/user-data/outputs/scheda_personaggio.pdf`.  
Edit the `canvas.Canvas(...)` path at the top of `build()` if you want a different output location.

With [just](https://github.com/casey/just):

```bash
just         # generate the PDF
just open    # generate and open in the default viewer
```

## Output

`scheda_personaggio.pdf` — single A4 page, ready to print or fill digitally.

## License

MIT
