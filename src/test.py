import csv
import networkx as nx

g = nx.DiGraph()


g.add_edge("Name1", "Name2")
nx.write_gexf(g, "tweets.gexf")
