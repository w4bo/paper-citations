import requests
import json
import yaml
import sys

with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)

resp = requests.get("http://api.elsevier.com/content/author?author_id=" + str(config["SCOPUS-ID"]) + "&view=metrics",
                    headers={'Accept': 'application/json', 'X-ELS-APIKey': config["SCOPUS-KEY"]})

# print(json.dumps(resp.json(), sort_keys=True, indent=4, separators=(',', ': ')))

resp = requests.get("http://api.elsevier.com/content/search/scopus?query=AU-ID(" + str(config["SCOPUS-ID"]) + ")",
                    # &field=dc:identifier&count=100
                    headers={'Accept': 'application/json', 'X-ELS-APIKey': config["SCOPUS-KEY"]})
results = resp.json()
papers = [r for r in results['search-results']["entry"]]

def get_scopus_info(SCOPUS_ID):
    url = ("http://api.elsevier.com/content/abstract/scopus_id/"
           + SCOPUS_ID
           + "?field=authors,title,publicationName,volume,issueIdentifier,prism:pageRange,coverDate,article-number,doi,citedby-count,prism:aggregationType")
    resp = requests.get(url, headers={'Accept':'application/json', 'X-ELS-APIKey': config["SCOPUS-KEY"]})
    results = json.loads(resp.text)
    print(results)
    #return results
    fstring = '"{title}","{journal}",{date},{citations}' # ,{volume},{articlenum}
    return fstring.format(authors=', '.join([au['ce:indexed-name'] for au in results['abstracts-retrieval-response']['authors']['author']]),
                          title=results['abstracts-retrieval-response']['coredata']['dc:title'],
                          journal=results['abstracts-retrieval-response']['coredata']['prism:publicationName'],
                          # volume=results['abstracts-retrieval-response']['coredata']['prism:volume'],
                          #articlenum=(results['abstracts-retrieval-response']['coredata'].get('prism:pageRange') or
                          #            results['abstracts-retrieval-response']['coredata'].get('article-number')),
                          date=results['abstracts-retrieval-response']['coredata']['prism:coverDate'],
                          # doi='doi:' + results['abstracts-retrieval-response']['coredata']['prism:doi'],
                          citations=int(results['abstracts-retrieval-response']['coredata']['citedby-count']))


def get_scopus_ref(SCOPUS_ID):
    url = "https://api.elsevier.com/content/search/scopus?query=refeid(" + SCOPUS_ID + ")"
    url = "https://api.elsevier.com/content/abstract/citations?eid=" + SCOPUS_ID + "&apikey=" + config["SCOPUS-KEY"]
    print(url)
    resp = requests.get(url, headers={'Accept': 'application/json', 'X-ELS-APIKey': config["SCOPUS-KEY"]})
    print(resp)
    results = json.loads(resp.text)
    return [entry for entry in results]
    # url = ("https://api.elsevier.com/content/abstract/scopus_id/"
    #        + SCOPUS_ID
    #        + "?view=REF")
    # resp = requests.get(url, headers={'Accept':'application/json', 'X-ELS-APIKey': config["SCOPUS-KEY"]})
    # results = json.loads(resp.text)
    # return [entry['title'] for entry in results['abstracts-retrieval-response']['references']['reference']]
    # # fstring = '{authors}, {title}, {journal}, {volume}, {articlenum}, ({date}). {doi} (cited {cites} times).\n'
    # fstring = '{authors}, {title}, {journal}, {volume}, {articlenum}, ({date}). (cited {cites} times).\n'
    # return fstring.format(authors=', '.join([au['ce:indexed-name'] for au in results['abstracts-retrieval-response']['authors']['author']]),
    #                       title=results['abstracts-retrieval-response']['coredata']['dc:title'],
    #                       journal=results['abstracts-retrieval-response']['coredata']['prism:publicationName'],
    #                       volume=results['abstracts-retrieval-response']['coredata']['prism:volume'],
    #                       articlenum=(results['abstracts-retrieval-response']['coredata'].get('prism:pageRange') or
    #                                   results['abstracts-retrieval-response']['coredata'].get('article-number')),
    #                       date=results['abstracts-retrieval-response']['coredata']['prism:coverDate'],
    #                       # doi='doi:' + results['abstracts-retrieval-response']['coredata']['prism:doi'],
    #                       cites=int(results['abstracts-retrieval-response']['coredata']['citedby-count']))

with open('scopus-citations.csv', 'w') as f:
    for p in papers:
        f.write(get_scopus_info("SCOPUS_ID:" + str(p["eid"].split("-")[-1])) + "\n")
        # print(get_scopus_info('SCOPUS_ID:85100942957'))
# print(get_scopus_ref('2-s2.0-85100942957'))