# Village Friends

Start with [DEVELOPMENT.md](DEVELOPMENT.md), the developer handoff. It links the editing guide for each system.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships. It covers the Java source, the Python authoring tools and the docs. `.graphifyignore` leaves out compiled assets, textures, sounds and the one-file-per-piece wardrobe and blueprint data.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- graphify may not be installed in a fresh session: `pip install graphifyy` (two y's) provides the `graphify` command. Without it, read graphify-out/GRAPH_REPORT.md.
- `graphify update .` refreshes code only. After changing the docs, rebuild their concepts with the graphify skill (`/graphify . --update`) and commit graphify-out/ with the change.
