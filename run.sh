#!/bin/bash
set -exo

jupyter nbconvert --execute --to notebook --inplace scopus-citations.ipynb
# jupyter nbconvert --execute --to notebook --inplace scholar-citations.ipynb
# jupyter nbconvert --execute --to notebook --inplace merge.ipynb