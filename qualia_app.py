import argparse
import json
from typing import Any, Dict, List, Optional

import numpy as np

from amne_compiler import AMNECompiler
from model import cnn_5d_to_3d


def fuse_architectures(
    text: str,
    context: List[str],
    tensor: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """
    Compile the AMNE pipeline and optionally fuse a tensor reduction.

    The fusion algorithm:
    1) Run AMNECompiler to obtain logical/telos metadata.
    2) If a tensor is provided, reduce it to a 3D signal.
    3) Combine both into a unified payload that includes a weighted score.
    """
    compiler = AMNECompiler()
    compilation = compiler.compile(text, context)

    tensor_payload: Optional[Dict[str, Any]] = None
    tensor_score = 0.0
    if tensor is not None:
        reduced = cnn_5d_to_3d(tensor)
        tensor_score = float(np.clip(reduced.mean(), 0.0, 1.0))
        tensor_payload = {
            "shape": reduced.shape,
            "mean_activation": round(float(reduced.mean()), 6),
            "max_activation": round(float(reduced.max()), 6),
        }

    telos_score = compilation["validation"]["telos_score"]
    fused_score = round((0.7 * telos_score) + (0.3 * tensor_score), 6)

    return {
        "compilation": compilation,
        "tensor": tensor_payload,
        "fused_score": fused_score,
    }


def parse_tensor(json_path: str) -> np.ndarray:
    with open(json_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return np.array(payload, dtype=float)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Qualia application: algorithmic fusion of AMNE + tensor reduction."
    )
    parser.add_argument("text", help="Input text to compile")
    parser.add_argument(
        "--context",
        nargs="*",
        default=[],
        help="Context terms to influence logic/telos evaluation",
    )
    parser.add_argument(
        "--tensor-json",
        help="Optional JSON file containing a 5D tensor (nested lists).",
    )

    args = parser.parse_args()
    tensor = parse_tensor(args.tensor_json) if args.tensor_json else None

    result = fuse_architectures(args.text, args.context, tensor)
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
