from java.awt import Color

# Node dicts
colors_nodes = {}

colors_nodes['tpc_'] = Color(0xFF4848)
colors_nodes['reviewer_'] = Color(0x26BA6C)
colors_nodes['author_'] = Color(0x3399FF)

colors_nodes['tpc_author_'] = Color(0x7238DB)
colors_nodes['tpc_reviewer_'] = Color(0x624E2F)
colors_nodes['tpc_reviewer_author_'] = Color(0xFFFFFF)
colors_nodes['reviewer_author_'] = Color(0x39B1CB)

size  = {}

size['tpc_'] = 25
size['reviewer_'] = 20
size['author_'] = 15

size['tpc_reviewer_author_'] = 60
size['tpc_reviewer_'] = 45
size['tpc_author_'] = 40
size['reviewer_author_'] = 35

node_keys = colors_nodes.keys()
for key in node_keys:
	g.filter(tag == key).nodes.color = colors_nodes[key]
	g.filter(tag == key).nodes.size = size[key]
	g.filter(level == key)


# Edge dicts
colors_edges = {}

colors_edges['institutional'] = Color(0x13F066)
colors_edges['paper'] = Color(0x2163C7)
colors_edges['social'] = Color(0xFFFFFF)

edge_keys = colors_edges.keys()
for key in edge_keys:
	print key
	g.filter(level == key).edges.color = colors_edges[key]

run_layout(FruchtermanReingold, 5000)