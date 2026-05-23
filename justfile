default: generate

# Ensure venv exists with dependencies
_venv:
    #!/usr/bin/env sh
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        .venv/bin/pip install reportlab
    fi

# Generate the character sheet PDF
generate: _venv
    .venv/bin/python scheda_v3.py

# Generate and open the PDF in the default viewer
open: generate
    open output/scheda_personaggio_v$(.venv/bin/python -c "from scheda_v3 import VERSION; print(VERSION)").pdf

# Create the venv and install dependencies
install:
    python3 -m venv .venv
    .venv/bin/pip install reportlab

# Create venv, install, and generate
setup: install generate
