#!/bin/bash
set -exo
jupyter nbconvert --execute --to notebook --inplace get-bib.ipynb
jupyter nbconvert --execute --to notebook --inplace scopus-citations.ipynb
jupyter nbconvert --execute --to notebook --inplace scholar-citations-serpapi.ipynb
jupyter nbconvert --execute --to notebook --inplace merge.ipynb