import os
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, DCTERMS, Namespace

from config import BASE_DIR, RDF_BASE_URL
from src.html_scraper import scrape_to_file
from src.clean_scraped import sections
from src.bin_clean import bin_clean

XMLF = "application/rdf+xml"

SWIVT = Namespace("http://semantic-mediawiki.org/swivt/1.0#")
WIKI = Namespace('http://www.skybrary.aero/index.php/Special:URIResolver/')
PROPERTY = Namespace(
    'http://www.skybrary.aero/index.php/Special:URIResolver/Property-3A')
WIKIURL = Namespace('https://www.skybrary.aero/index.php/')
SIOC = Namespace("http://rdfs.org/sioc/ns#")


NAMESPACES = dict(swivt=SWIVT,
                  wiki=WIKI,
                  property=PROPERTY,
                  wikiurl=WIKIURL,
                  sioc=SIOC,
                  dcterms=DCTERMS,
                  )

RDF_DIR = os.path.join(BASE_DIR, "rdf")


class Ontology(Graph):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for ns, uri in NAMESPACES.items():
            self.bind(ns, uri)

    def load_new_rdf(self):
        self.injest_container()
        self.injest_reports()

    def load_new_html(self):
        print("Finding URLs")
        for r in self.query("""SELECT DISTINCT ?url
                            WHERE {
                               ?url a swivt:Subject.
                            }"""
                           ):
            title, content = scrape_to_file(r.url)
            if title is not None:
                self.add_title(r.url, title, content)
        print("Length after html: {}".format(self.__len__()))

    def categorise_files(self):
        mkurl = "http://www.skybrary.aero/index.php/Special:URIResolver/{}".format
        triples = []
        for category in bin_clean():
            url = mkurl(category.filename.replace('+','/')[:-4])
            triples.append((URIRef(url), DCTERMS.subject, Literal(category.subject)))
            for topic in category.bins:
                triples.append((URIRef(url), SIOC.topic, Literal(topic)))
        self.add_triples(triples)
        print("Length after categorising: {}".format(self.__len__()))

    def injest_container(self):
        print("Injesting from Skybrary")
        self.parse(RDF_BASE_URL, format=XMLF)
        print("Length after injesting container: {}".format(self.__len__()))

    def injest_reports(self):
        print("Beginning to injest all reports...")
        for r in self.query("""SELECT DISTINCT ?u
                            WHERE {
                            ?s a swivt:Subject.
                            ?s rdfs:isDefinedBy ?u.
                            }"""
                            ):
            self.parse(r.u, format=XMLF)
        print("Length after injesting reports: {}".format(self.__len__()))

    def write_out_rdf(self):
        print("Writing out to file")
        with open(os.path.join(RDF_DIR, "skybrary.rdf"), 'w') as rdf_file:
            rdf_file.write(self.serialize(format="pretty-xml").decode('utf-8'))

    def add_title(self, url, title, content):
        cleaned_content = "\n".join(sections(content.splitlines()))
        triples = [(URIRef(url), DCTERMS.title, Literal(title[:-4])),
                   (URIRef(url), SIOC.content, Literal(cleaned_content)),
                   ]
        self.add_triples(triples)

    def add_triples(self, triples):
        for triple in triples:
            self.add(triple)
