# Skybrary Data

## Requirements

Requirements are all Python3.6+ and can be installed with pip:

```
pip install -r requirements.txt
```

## Running the app
The main entry point to the application is `run.py`, which accepts two
command line flags:

* `--injest` : This will download and store all the required RDF from Skybrary,
             which is required for the first run.
* `--noweb`  : Prevents the web server from running, which at the moment is just
               the Flask development server.

For the **first** run use:

```
python3.6 run.py --injest
```

Then use:

```
python3.6 run.py
```

The visualisation also requires `serve_vis.sh` to be run, this runs the bokeh
server without you needing to remember all the flags it needs.

```
bash serve_vis.sh
```

### Note
Be aware that currently all the data is loaded into memory with rdflib, this
operation takes a second so keep an eye on your command line to know when
the application is ready to use. The advantage of this is the application is
pure Python, no need for an external data base and once the data is loaded it
is adequately fast.

## Querying the data

In a browser go to <http://127.0.0.1:5000>, this is the home page and query page.
You can input SPARQL queries here, some prefixes have been predefined for you.

### Note
If you try to query all the triples the application may crash, there are a lot
of triples in the data!

### An example query:
This will return flights that suffered from a loss of control on their way
to London Heathrow Airport:

```sparql
SELECT ?flight ?type_of_flight ?phase_of_flight ?loss_of_control ?synopsis
WHERE {
    ?flight rdf:type swivt:Subject .
    ?flight wiki:Property-3AFlight_Intended_Destination wiki:EPWA .
    ?flight wiki:Property-3AType_of_Flight ?type_of_flight .
    ?flight wiki:Property-3APhase_of_Flight ?phase_of_flight .
    ?flight wiki:Property-3ALOC ?loss_of_control .
    ?flight wiki:Property-3ASynopsis ?synopsis .
}
```

## Visualising the data
This is not yet interactive and it struggles to visualise all the triples. On my
machine it takes 20 minutes to generate such a plot. As such it is suggested
to keep the query that generates the data for the plot to one that returns
only a small subset of triples.

There's much work to be done on this tool. But for now you can update the
query in `visapp.py`, be aware you may also have to update the code that
parses it into a networkx graph there too.

The route to view the visualisation, which by default gives all the triples
associated with flights that were intended to travel to London Heathrow, is
<http://127.0.0.1:5000/vis>.
