from scholarly import scholarly
import yaml
import time

with open("config.yml") as stream:
    config = yaml.safe_load(stream)

print("Author id: " + config["SCHOLAR-ID"])

# Retrieve the author's data, fill-in, and print
search_query = scholarly.search_author(config["SCHOLAR-ID"])
author = scholarly.fill(next(search_query))
print(author)

# Print the titles of the author's publications
# print([pub['bib']['title'] for pub in author['publications']])

with open('scholar-citations.csv', 'w') as f:
    for p in author['publications']:
        pub = scholarly.fill(p)
        f.write('"' + pub['bib']['title'] + '"' + "," + str(pub['bib']['pub_year']) + "," + str(pub['num_citations']) + "\n")   
        # Which papers cited that publication?
        # citations = [citation['bib']['title'] for citation in scholarly.citedby(pub)]
        # print(citations)
        # for c in citations:
        #     f.write(pub['bib']['title'] + "," + c + "\n")
        #     f.flush()
        # time.sleep(1)
