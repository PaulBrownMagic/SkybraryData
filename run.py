#!/usr/bin/env python3

import argparse
import os
import sys

from config import BASE_DIR
from src import Ontology, clean_files

description = """Data management for Skybrary Data. Injests and cleans data."""

parser = argparse.ArgumentParser(description=description)

parser.add_argument('--injest',
                    action='store_true',
                    help="Download data from Skybrary")
parser.add_argument('--noparse',
                    action='store_true',
                    help="Don't parse data")
parser.add_argument('--scrape',
                    action='store_true',
                    help="Scrape html to txt for Skybrary reports")
parser.add_argument('--bin',
                    action='store_true',
                    help="Put data into bins")
parser.add_argument('--update',
                    action='store_true',
                    help="Don't add new data to rdf")
parser.add_argument('--offline', action='store_true',
                    help="All offline tasks")
parser.add_argument('--all', action='store_true',
                    help="Complete refresh")

def exit():
    print("Exiting")
    sys.exit(0)

if __name__ == "__main__":
    args = parser.parse_args()
    ontology = Ontology()
    if args.injest or args.all:
        print("Injesting Data")
        ontology.load_new_rdf()
    else:
        print("Loading data")
        ontology.parse(os.path.join(BASE_DIR, "rdf", "skybrary.rdf"))
        print("Length of graph: {}".format(len(ontology)))
    if args.noparse:
        exit()
    if args.scrape or args.all or args.offline:
        if not args.offline:
            print("Scraping from Skybrary HTML to text")
            ontology.load_new_html()
        print("Cleaning docs")
        clean_files()
    if args.bin or args.all or args.offline:
        print("Putting docs into bins")
        ontology.categorise_files()
    if args.update or args.all or args.offline:
        print("Updating RDF")
        ontology.write_out_rdf()
    exit()
