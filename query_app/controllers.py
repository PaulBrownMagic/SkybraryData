#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Routes for app."""

from functools import partial

from bokeh.embed import server_document
from bs4 import BeautifulSoup
from flask import render_template, request, flash
from requests import post, codes

from .forms import SPARQLform
from .flask_app import app
from .models import Graph, NAMESPACES


graph = Graph()


@app.template_filter('namespace')
def abbreviate(url):
    for abbr, ns in NAMESPACES.items():
        if str(ns) in url:
            return url.replace(str(ns), f"{abbr}:")
    return url


@app.route("/", methods=["GET"])
def home_page():
    """Render the home page."""
    return render_template("home.html",
                           namespaces=NAMESPACES,
                           form=SPARQLform())


@app.route("/", methods=["POST"])
def result_page():
    """Render the query result."""
    if not SPARQLform().validate_on_submit():
        flash("Invalid Query")
        return home_page()
    query = request.form.get('query')
    try:
        results = graph.query(query)
    except Exception as e:
        flash("Could not run that query.")
        flash(f"RDFLIB Error: {e}")
        sparql_validate(query)
        return home_page()
    return render_template("result.html",
                           namespaces=NAMESPACES,
                           form=SPARQLform(),
                           results=results)


@app.route("/vis")
def visualise():
    script = server_document("http://127.0.0.1:5006/visapp")
    return render_template("vis.html",
                           script=script)


def sparql_validate(query):
    prefixes = """PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
PREFIX swivt:   <http://semantic-mediawiki.org/swivt/1.0#>
PREFIX wiki:    <http://www.skybrary.aero/index.php/Special:URIResolver/>
PREFIX property: <http://www.skybrary.aero/index.php/Special:URIResolver/Property-3A>
PREFIX wikiurl: <https://www.skybrary.aero/index.php/>

"""
    query = prefixes + query
    print(query)
    data = {"query": query}
    resp = post("http://sparql.org/validate/query", data=data)
    if resp.status_code == codes.ok:
        soup = BeautifulSoup(resp.content.decode('utf-8'), "html.parser")
        pres = soup.find_all('pre')
        for p in pres:
            flash(p)
