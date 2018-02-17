#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Download all the RDF data in Skybrary's Accident and Incident Category.

Saves data in one big RDF+XML file.
"""

import os
import rdflib
from rdflib.namespace import RDF, RDFS, OWL, Namespace

from config import BASE_DIR

SWIVT = Namespace("http://semantic-mediawiki.org/swivt/1.0#")
WIKI = Namespace('http://www.skybrary.aero/index.php/Special:URIResolver/')
PROPERTY = Namespace(
    'http://www.skybrary.aero/index.php/Special:URIResolver/Property-3A')
WIKIURL = Namespace('https://www.skybrary.aero/index.php/')

RDF_DIR = os.path.join(BASE_DIR, "rdf")


def injest_data():
    """Download all RDF from Skybrary.

    Downloads the initial container rdf+xml file, parses into an rdflib graph.
    Then downloads the individual accident/incident rdf+xml files and parses
    them into the rdflib graph. Finally it serialises them into a data.rdf
    rdf_xml file.
    """
    graph = rdflib.Graph()
    print("Injesting")
    # graph.parse(os.path.join(RDF_DIR, "container.rdf"),
    graph.parse(
        "https://www.skybrary.aero/index.php/Special:ExportRDF/Category:Accidents_and_Incidents",
        format="application/rdf+xml")
    print("Graph length after ingesting container", len(graph))

    qres = graph.query("""SELECT DISTINCT ?u
                       WHERE {
                       ?s rdf:type swivt:Subject .
                       ?s rdfs:isDefinedBy ?u .
                       }""",
                       initNs=dict(swivt=SWIVT)
                       )
    print("Beginning to injest all reports...")
    for r in qres:
        graph.parse(r.u, format="application/rdf+xml")
    print("Graph length after ingesting everything", len(graph))
    with open(os.path.join(RDF_DIR, "skybrary.rdf"), 'w') as rdf_file:
        rdf_file.write(graph.serialize(format="pretty-xml").decode('utf-8'))
    print("Saved to file")


if __name__ == "__main__":
    injest_data()
