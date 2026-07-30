Given a Python code base build a tool that allows to visualize code,

parse the code (see how functions interact, objects) animated, click to follow
the code Different levels of abstractions

a representation in python of a python code base, e.g., how functions relate to
each other in a visual form through a graph, correlate structure of the code with
the code of each function, use multiple level of abstractions (file level, module
level)

# Parsing / static analysis

libcst — like ast but preserves exact formatting/whitespace and gives you a full concrete syntax tree. Better if you want to show/highlight actual source snippets per node rather than just structural facts.
astroid (what pylint is built on) — does type/name inference, so it can resolve self.foo() or imported names to their actual definitions much better than raw ast. This is usually the difference between a call graph that's "roughly right" and one that's actually usable.
jedi — static analysis engine with "go to definition" / "find references" built in; handy for resolving cross-file/cross-module call edges without writing your own resolver.
grimp — purpose-built for building import graphs at package/module level (used by import-linter). Great for the "module level" layer of your abstraction stack.

# Call / dependency graph generator

code2flow — generates function-level call graphs across a whole codebase, outputs to Graphviz DOT or JSON. Good starting point/reference implementation.
pydeps — module-level dependency graphs via Graphviz.
pyreverse (bundled with pylint) — UML-style class diagrams (inheritance, composition).

# Visualization

Graphviz (graphviz or pygraphviz python bindings) — subgraph cluster_* blocks map naturally to your file/module grouping. Best for static, clean hierarchical diagrams.
dash-cytoscape (Cytoscape.js in Dash) — supports compound nodes (nodes containing nodes), which is exactly the file→class→function nesting you want, plus expand/collapse and click-to-drill-down. This is probably your best bet for genuinely multi-level interactive exploration.
pyvis — quick interactive HTML graphs (vis.js), less structured than Cytoscape but very fast to get something clickable.
