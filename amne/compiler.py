#!/usr/bin/env python3
"""AMNE compiler: natural language relation lines -> ontology graph."""

import argparse
import json
from pathlib import Path

from lark import Lark, Transformer

GRAMMAR_PATH = Path(__file__).with_name("grammar.lark")

VOCABULARY = {
    "שכל פועל": "amne:ActiveIntellect",
    "נבואי": "amne:Prophetic",
    "צירוף": "amne:Conjunction",
    "נמצא": "amne:Exists",
}


class GraphBuilder(Transformer):
    def __init__(self) -> None:
        self.triples = []

    def statement(self, items):
        s, r, o = [str(i).strip() for i in items]
        self.triples.append((s, r, o))
        return items


def compile_text(text: str) -> dict:
    parser = Lark(GRAMMAR_PATH.read_text(encoding="utf-8"), parser="lalr")
    tree = parser.parse(text)
    builder = GraphBuilder()
    builder.transform(tree)

    nodes = sorted({x for t in builder.triples for x in (t[0], t[2])})
    edges = [
        {"source": s, "relation": r, "target": o, "iri": VOCABULARY.get(r, f"amne:{r}")}
        for s, r, o in builder.triples
    ]

    return {"nodes": nodes, "edges": edges, "vocabulary": VOCABULARY}


def to_jsonld(graph: dict) -> dict:
    return {
        "@context": {
            "amne": "https://qualia.local/amne#",
            "relation": "amne:relation",
            "source": "amne:source",
            "target": "amne:target",
        },
        "@graph": [
            {
                "@id": f"amne:{edge['source'].replace(' ', '_')}_{idx}",
                "source": edge["source"],
                "relation": edge["iri"],
                "target": edge["target"],
            }
            for idx, edge in enumerate(graph["edges"], start=1)
        ],
    }


def to_rdf_turtle(graph: dict) -> str:
    lines = ["@prefix amne: <https://qualia.local/amne#> ."]
    for edge in graph["edges"]:
        src = edge["source"].replace(" ", "_")
        tgt = edge["target"].replace(" ", "_")
        pred = edge["iri"].split(":", 1)[1]
        lines.append(f"amne:{src} amne:{pred} amne:{tgt} .")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-dir", default="build")
    args = ap.parse_args()

    src = Path(args.input).read_text(encoding="utf-8")
    graph = compile_text(src)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "graph.jsonld").write_text(json.dumps(to_jsonld(graph), ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "graph.ttl").write_text(to_rdf_turtle(graph), encoding="utf-8")

    print(f"Compiled graph with {len(graph['edges'])} triples into {out_dir}")


if __name__ == "__main__":
    main()
