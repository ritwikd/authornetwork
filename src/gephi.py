from java.awt import Color


g.filter(tag == 'tpc_').nodes.color = Color(0xFF4848)
g.filter(tag == 'reviewer_').nodes.color = Color(0x26BA6C)
g.filter(tag == 'author_').nodes.color = Color(0x3399FF)

g.filter(tag == 'tpc_author_').nodes.color = Color(0x7238DB)
g.filter(tag == 'tpc_reviewer_').nodes.color = Color(0x624E2F)
g.filter(tag == 'tpc_reviewer_author_').nodes.color = Color(0xFFFFFF)
g.filter(tag == 'reviewer_author_').nodes.color = Color(0x39B1CB)

g.filter(tag == 'tpc_').nodes.size = 25
g.filter(tag == 'reviewer_').nodes.size = 20
g.filter(tag == 'author_').nodes.size = 15

g.filter(tag == 'tpc_reviewer_author_').nodes.size = 60
g.filter(tag == 'tpc_reviewer_').nodes.size = 45
g.filter(tag == 'tpc_author_').nodes.size = 40
g.filter(tag == 'reviewer_author_').nodes.size = 35

g.filter(level == 'institutional').edges.color = Color(0x13F066)
g.filter(level == 'paper').edges.color = Color(0x2163C7)
g.filter(level == 'social').edges.color = Color(0xFFFFFF)


run_layout(FruchtermanReingold, 5000)