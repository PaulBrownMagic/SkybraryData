#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""RDF functions on Skybrary Data."""

import os
import rdflib
from rdflib.namespace import RDF, RDFS, OWL, Namespace

from config import BASE_DIR

SWIVT = Namespace("http://semantic-mediawiki.org/swivt/1.0#")
WIKI = Namespace('http://www.skybrary.aero/index.php/Special:URIResolver/')
PROPERTY = Namespace(
    'http://www.skybrary.aero/index.php/Special:URIResolver/Property-3A')
WIKIURL = Namespace('https://www.skybrary.aero/index.php/')

NAMESPACES = dict(swivt=SWIVT,
                  wiki=WIKI,
                  property=PROPERTY,
                  wikiurl=WIKIURL,
                  rdf=RDF,
                  rdfs=RDFS,
                  owl=OWL)

RDF_DIR = os.path.join(BASE_DIR, "rdf")


class Graph:
    """Interface to rdflib graph."""
    graph = rdflib.Graph()
    print("Loading data")
    graph.parse(os.path.join(RDF_DIR, "skybrary.rdf"))
    print("Data loaded")

    def query(self, q):
        """Allow user query."""
        return self.graph.query(q, initNs=NAMESPACES)
