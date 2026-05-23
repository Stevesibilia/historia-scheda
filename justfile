default: generate

# Generate the character sheet PDF
generate:
    python scheda_v3.py

# Generate and open the PDF in the default viewer
open: generate
    open /mnt/user-data/outputs/scheda_personaggio.pdf

# Install Python dependencies
install:
    pip install reportlab

# Install dependencies and generate
setup: install generate
