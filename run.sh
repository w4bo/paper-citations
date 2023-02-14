#!/bin/bash
set -exo
if [[ -d venv/Scripts ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

python scopus-citations.py
jupyter nbconvert --execute --to notebook --inplace scholar-citations.ipynb
jupyter nbconvert --execute --to notebook --inplace merge.ipynb