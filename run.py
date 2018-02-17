#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Injest Data or Run the SPARQL Query webapp."""

import argparse

from ingest_data import injest_data
from query_app import app

description = """Skybrary RDF data interface. Runs the webserver for SPARQL
queries on the downloaded, serialised RDF data from Skybrary by default. Can
also be used to update the data, note this operation clobbers the old data."""
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--injest', action='store_true',
                    help='Injest new data.')
parser.add_argument('--noweb', action='store_false',
                    help='Do NOT start the webserver.')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.injest:
        injest_data()
    if args.noweb:
        app.run()
