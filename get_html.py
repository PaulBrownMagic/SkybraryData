from bs4 import BeautifulSoup
from itertools import chain
import os
import rdflib
from rdflib.namespace import RDF, RDFS, OWL, Namespace
import requests

from config import BASE_DIR

SWIVT = Namespace("http://semantic-mediawiki.org/swivt/1.0#")
WIKI = Namespace('http://www.skybrary.aero/index.php/Special:URIResolver/')
PROPERTY = Namespace(
    'http://www.skybrary.aero/index.php/Special:URIResolver/Property-3A')
WIKIURL = Namespace('https://www.skybrary.aero/index.php/')

RDF_DIR = os.path.join(BASE_DIR, "rdf")

def is_valid_resp(resp):
    return resp.status_code == requests.codes.ok

def get_html(resp):
    soup =  BeautifulSoup(resp.content).body
    txt = "\n".join([t.string for t in soup.select(".mw-headline")[0].parent.next_siblings])
    print(txt)
    return txt

def scrape_to_file(url):
    print("URL: ", url)
    res = requests.get(url)
    if not is_valid_resp(res):
        print("INVALID RESPONSE", url)
    else:
        txt = get_html(res)
        fname = f"{url.split('/')[-1]}.txt"
        with open(os.path.join(BASE_DIR, "scraped", fname), "w") as of:
            print(txt, file=of)



def injest_data():
    graph = rdflib.Graph()
    print("Reading Data")
    graph.parse(os.path.join(BASE_DIR, "rdf", "skybrary.rdf"))
    print("Data Loaded")
    print("Finding URLs")
    qres = graph.query("""SELECT DISTINCT ?url
                       WHERE {
                       ?url a swivt:Subject.
                       } LIMIT 1""",
                       initNs=dict(swivt=SWIVT)
                       )
    print("Beginning injesting")
    for row in qres:
        scrape_to_file(row.url)
    print("Complete")

if __name__ == "__main__":
    injest_data()
