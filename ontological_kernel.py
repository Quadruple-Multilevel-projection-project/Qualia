import os
from typing import Dict, Any

import numpy as np
from flask import Flask, jsonify, request

from amne_compiler import AbulafiaMapper

app = Flask(__name__)


class PathSevenKernel:
    """ליבה אונטולוגית שמאגדת את שבע השכבות לעיבוד חכם."""

    def __init__(self) -> None:
        self.alphabet = "אבגדהוזחטיכלמנסעפצקרשת"
        self.mapper = AbulafiaMapper()

    def process(self, text: str) -> Dict[str, Any]:
        fused = "".join([c for c in text if c in self.alphabet])
        sod_hidden = sum(self.mapper.encode(fused))
        integrity = "VALID" if len(fused) > 1 else "INVALID_PALACE"
        prophetic_vector = float(np.tanh(sod_hidden / 100))

        return {
            "fused": fused,
            "sod": sod_hidden,
            "status": integrity,
            "prophetic_vector": prophetic_vector,
        }


kernel = PathSevenKernel()


@app.route("/analyze", methods=["POST"])
def analyze() -> Any:
    data = request.json or {}
    result = kernel.process(data.get("text", ""))
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
