# tk-netgraph
tk-netgraph is a powerful graph engine for tkinter that prioritizes modularity and customization. It is 
currently in a WIP-state and actively maintained.

The following features are supported right now:
- Multigraphs (multiple edges with the same endpoints)
- self-loops (edges that connect a node to itself)
- Labeled and weighted edges
- Labeled nodes
- Dragging of nodes
- Dragging of graph components or the whole graph
- Dynamic edge creation by clicking on nodes
- Cheap antialiased circles/lines (wip)
- Appearance configuration

Missing:
- support for directed edges
- not all configuration options are accounted for (e.g. can not disable antialiasing)
- API is missing some abstract components 