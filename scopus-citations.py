import requests
import json
import yaml
import sys

with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)

resp = requests.get("http://api.elsevier.com/content/author?author_id=" + str(config["SCOPUS-ID"]) + "&view=metrics",
                    headers={'Accept': 'application/json', 'X-ELS-APIKey': config["SCOPUS-KEY"]})

print(json.dumps(resp.json(), sort_keys=True, indent=4, separators=(',', ': ')))

resp = requests.get("http://api.elsevier.com/content/search/scopus?query=AU-ID(" + str(config["SCOPUS-ID"]) + ")",
                    # &field=dc:identifier&count=100
                    headers={'Accept': 'application/json', 'X-ELS-APIKey': config["SCOPUS-KEY"]})
results = resp.json()
papers = [str(r) for r in results['search-results']["entry"]]
print(papers)

def get_scopus_info(SCOPUS_ID):
    url = ("http://api.elsevier.com/content/abstract/scopus_id/"
           + SCOPUS_ID
           + "?field=authors,title,publicationName,volume,issueIdentifier,prism:pageRange,coverDate,article-number,doi,citedby-count,prism:aggregationType")
    resp = requests.get(url,
                        headers={'Accept':'application/json', 'X-ELS-APIKey': config["SCOPUS-KEY"]})
    results = json.loads(resp.text.encode('utf-8'))
    return results
    # fstring = '{authors}, {title}, {journal}, {volume}, {articlenum}, ({date}). {doi} (cited {cites} times).\n'
    fstring = '{authors}, {title}, {journal}, {volume}, {articlenum}, ({date}). (cited {cites} times).\n'
    return fstring.format(authors=', '.join([au['ce:indexed-name'] for au in results['abstracts-retrieval-response']['authors']['author']]),
                          title=results['abstracts-retrieval-response']['coredata']['dc:title'].encode('utf-8'),
                          journal=results['abstracts-retrieval-response']['coredata']['prism:publicationName'].encode('utf-8'),
                          volume=results['abstracts-retrieval-response']['coredata']['prism:volume'].encode('utf-8'),
                          articlenum=(results['abstracts-retrieval-response']['coredata'].get('prism:pageRange') or
                                      results['abstracts-retrieval-response']['coredata'].get('article-number')).encode('utf-8'),
                          date=results['abstracts-retrieval-response']['coredata']['prism:coverDate'].encode('utf-8'),
                          # doi='doi:' + results['abstracts-retrieval-response']['coredata']['prism:doi'].encode('utf-8'),
                          cites=int(results['abstracts-retrieval-response']['coredata']['citedby-count'].encode('utf-8')))


def get_scopus_ref(SCOPUS_ID):
    url = "https://api.elsevier.com/content/search/scopus?query=refeid(" + SCOPUS_ID + ")"
    url = "https://api.elsevier.com/content/abstract/citations?eid=" + SCOPUS_ID + "&apikey=" + config["SCOPUS-KEY"]
    print(url)
    resp = requests.get(url, headers={'Accept': 'application/json', 'X-ELS-APIKey': config["SCOPUS-KEY"]})
    print(resp)
    results = json.loads(resp.text.encode('utf-8'))
    return [entry for entry in results]
    # url = ("https://api.elsevier.com/content/abstract/scopus_id/"
    #        + SCOPUS_ID
    #        + "?view=REF")
    # resp = requests.get(url, headers={'Accept':'application/json', 'X-ELS-APIKey': config["SCOPUS-KEY"]})
    # results = json.loads(resp.text.encode('utf-8'))
    # return [entry['title'] for entry in results['abstracts-retrieval-response']['references']['reference']]
    # # fstring = '{authors}, {title}, {journal}, {volume}, {articlenum}, ({date}). {doi} (cited {cites} times).\n'
    # fstring = '{authors}, {title}, {journal}, {volume}, {articlenum}, ({date}). (cited {cites} times).\n'
    # return fstring.format(authors=', '.join([au['ce:indexed-name'] for au in results['abstracts-retrieval-response']['authors']['author']]),
    #                       title=results['abstracts-retrieval-response']['coredata']['dc:title'].encode('utf-8'),
    #                       journal=results['abstracts-retrieval-response']['coredata']['prism:publicationName'].encode('utf-8'),
    #                       volume=results['abstracts-retrieval-response']['coredata']['prism:volume'].encode('utf-8'),
    #                       articlenum=(results['abstracts-retrieval-response']['coredata'].get('prism:pageRange') or
    #                                   results['abstracts-retrieval-response']['coredata'].get('article-number')).encode('utf-8'),
    #                       date=results['abstracts-retrieval-response']['coredata']['prism:coverDate'].encode('utf-8'),
    #                       # doi='doi:' + results['abstracts-retrieval-response']['coredata']['prism:doi'].encode('utf-8'),
    #                       cites=int(results['abstracts-retrieval-response']['coredata']['citedby-count'].encode('utf-8')))
# print(get_scopus_info(papers[0]))
# print(get_scopus_info('SCOPUS_ID:85100942957'))
print(get_scopus_ref('2-s2.0-85100942957'))