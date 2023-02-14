import pybliometrics
from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus.utils import config
from pybliometrics.scopus import AuthorRetrieval
import sys
import pandas as pd
import time

s = ScopusSearch("AU-ID(56344636600)")
my_papers = s.results
my_papers = [[x.title, x.eid, x.doi] for x in my_papers]

acc = []
for paper in my_papers:
    q = f"REF({paper[1]})"
    s = ScopusSearch(q)
    res = s.results
    if res is not None and len(res) > 0:
        for x in res:
            acc = acc + [paper + [x.title, x.eid, x.doi]]
    else:
        acc = acc + [paper + ["", "", ""]]

df = pd.DataFrame(acc, columns=["Paper title", "Paper eid", "Paper doi", "Citing paper title", "Citing paper eid", "Citing paper doi"])
df.to_csv("data/scopus-citations-{}.csv".format(time.time()), index=False)