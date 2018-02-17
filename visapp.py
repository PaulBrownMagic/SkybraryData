

from random import random

from bokeh.layouts import column
from bokeh.models import Button, Plot, Range1d, MultiLine, Circle
from bokeh.models import HoverTool, TapTool, WheelZoomTool
from bokeh.models import PanTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx
from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, curdoc, output_file, save
import networkx as nx

from query_app import graph as sparql
from query_app import abbreviate

data = sparql.query("""SELECT DISTINCT ?s ?p ?o
                    WHERE { ?s a swivt:Subject .
                            ?s wiki:Property-3AFlight_Intended_Destination wiki:EPWA .
                            ?s ?p ?o .
                    }""")

print("Converting Data")
graph = nx.Graph()
for row in data:
    s = abbreviate(str(row.s))
    o = abbreviate(str(row.o))
    p = abbreviate(str(row.p))
    graph.add_node(s, lbl=s)
    graph.add_node(o, lbl=o)
    graph.add_edge(s, o, predicate=p)

predicates = [w for u, v, w in graph.edges.data('predicate')]
adjacencies = list()
for o in graph.adj.values():
    adj = ""
    for k, v in o.items():
        adj += f"<li>{v['predicate']} {k} </li>"
    adjacencies.append(adj)

print("Making Plot")
plot = Plot(plot_width=600, plot_height=600,
            x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1),
            output_backend="webgl")
plot.title.text = "Flights to London Heathrow"

tips = """
<div>
    <div>
        <h4>Info</h4>
        <p>@uri</p>
    </div>
    <div>
        <ul>
            @adj{safe}
        </ul>
    </div>
</div>
"""

plot.add_tools(HoverTool(tooltips=tips),
               TapTool(),
               PanTool(),
               WheelZoomTool(),
               BoxZoomTool(),
               ResetTool()
               )

graph_renderer = from_networkx(graph, nx.spring_layout, scale=1, center=(0,0))
graph_renderer.selection_policy = EdgesAndLinkedNodes()
graph_renderer.inspection_policy = NodesAndLinkedEdges()

graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
graph_renderer.node_renderer.selection_glyph = Circle(size=15,
                                                      fill_color=Spectral4[2])
graph_renderer.node_renderer.hover_glyph = Circle(size=15,
                                                  fill_color=Spectral4[1])
graph_renderer.node_renderer.data_source.data['uri'] = list(graph.nodes)
graph_renderer.node_renderer.data_source.data['adj'] = adjacencies

graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC",
                                               line_alpha=0.8,
                                               line_width=5)
graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2],
                                                         line_width=5)
graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1],
                                                     line_width=5)


plot.renderers.append(graph_renderer)
# print("Saving Plot")
# output_file("query_app/templates/includes/plot.html")
# save(plot)
print("Serving Plot")
# put the button and plot in a layout and add to the document
curdoc().add_root(column(plot))
