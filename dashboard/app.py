#!/usr/bin/env python3
import json
from pathlib import Path

import dash
from dash import html
import dash_cytoscape as cyto

GRAPH_FILE = Path("build/graph.json")


def load_graph():
    if not GRAPH_FILE.exists():
        return {"nodes": [], "edges": []}
    return json.loads(GRAPH_FILE.read_text(encoding="utf-8"))


def tension_lambda2(graph: dict) -> float:
    # Heuristic tension proxy: relation density over nodes.
    nodes = max(len(graph.get("nodes", [])), 1)
    edges = len(graph.get("edges", []))
    return round(edges / nodes, 3)


def to_cytoscape(graph: dict):
    elements = [{"data": {"id": n, "label": n}} for n in graph["nodes"]]
    for i, e in enumerate(graph["edges"], start=1):
        elements.append(
            {
                "data": {
                    "id": f"edge-{i}",
                    "source": e["source"],
                    "target": e["target"],
                    "label": e["relation"],
                }
            }
        )
    return elements


graph = load_graph()
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H2("AMNE Semantic Dashboard"),
        html.Div(f"Tension Gauge λ₂: {tension_lambda2(graph)}", style={"fontWeight": "bold"}),
        cyto.Cytoscape(
            id="ontology-graph",
            layout={"name": "cose"},
            style={"width": "100%", "height": "700px"},
            elements=to_cytoscape(graph),
            stylesheet=[
                {"selector": "node", "style": {"label": "data(label)", "background-color": "#1f77b4"}},
                {"selector": "edge", "style": {"label": "data(label)", "curve-style": "bezier", "target-arrow-shape": "triangle"}},
            ],
        ),
    ]
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
