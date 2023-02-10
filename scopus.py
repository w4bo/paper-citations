import pybliometrics
from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus.utils import config
print(config['Authentication']['APIKey'])
config['Authentication']['APIKey'] = "4282c4bc758424489c7023b2b05b5773"
print(config['Authentication']['APIKey'])

cited = "2-s2.0-85107683405"
q = f"REF({cited})"
s = ScopusSearch(q)
citing = s.results
print(citing)