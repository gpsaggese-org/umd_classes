In tutorials/dowhy/dowhy_API_utils.py

Factor out the style used for these functions in a function

    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=node_color,
        node_size=2000,
        edgecolors="black",
        ax=ax,
    )
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color=edge_color,
        arrowsize=20,
        arrowstyle="-|>",
        width=1.8,
        ax=ax,
    )

so that the all plots look the same

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications

- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`
- When writing a notebook follow `.claude/skills/notebook.rules.md`
