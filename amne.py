"""AMNE — Meta-Algorithm (Algorithm-of-Algorithms).

This module composes lower-level primitives and modules step-by-step and
produces a derivation trace that explains how the final engine was built.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any, Callable, Dict, List, Tuple


class DerivationTrace:
    """Collects derivation entries for algorithm assembly."""

    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = []

    def add(self, stage: str, rationale: str, artifact: Dict[str, Any] | None = None) -> None:
        self.entries.append(
            {
                "stage": stage,
                "rationale": rationale,
                "artifact": artifact or {},
            }
        )

    def dump(self) -> List[Dict[str, Any]]:
        return self.entries


def assemble_letter_mapper(
    weights: Dict[str, int] | None = None,
) -> Tuple[Callable[[str], Tuple[int, List[int], str]], Dict[str, Any]]:
    """Assemble the Abulafia primitive: map Hebrew text -> numerical vector + signature.

    Returns:
      - encode(text) -> (total, vector, signature)
      - artifact metadata
    """

    def encode(text: str) -> Tuple[int, List[int], str]:
        vals = [ord(ch) - ord("\u05d0") + 1 for ch in text if "\u05d0" <= ch <= "\u05ea"]
        if weights:
            vals = [v + weights.get(chr(ord("\u05d0") + v - 1), 0) for v in vals]
        total = sum(vals)
        signature = hashlib.md5(text.encode("utf-8")).hexdigest()
        return total, vals, signature

    artifact = {"type": "LetterMapper", "weights": weights or {}}
    return encode, artifact


def assemble_maimonides_filter(
    theta: float = 0.7,
) -> Tuple[Callable[[str, str], bool], Dict[str, Any]]:
    """Assemble a minimal Maimonidean equivocation check primitive.

    validate(a,b) -> bool (True = OK / not equivocal)
    """

    def validate(a: str, b: str, encode_func: Callable[[str], Tuple[int, List[int], str]] | None = None) -> bool:
        if encode_func is None:
            # fallback simple: compare normalized lengths
            return (len(a) == 0 or len(b) == 0) and True
        sa = encode_func(a)[0]
        sb = encode_func(b)[0]
        if sa == 0 or sb == 0:
            return True
        ratio = min(sa, sb) / max(sa, sb)
        return ratio < theta

    artifact = {"type": "MaimonidesFilter", "theta": theta}
    return validate, artifact


def assemble_interpretive_parser() -> Tuple[Callable[[str], List[str]], Dict[str, Any]]:
    """Simple, conservative parser: splits text into clauses/units.

    Returns split(text) -> List[units]
    """
    import re

    splitter = re.compile(r"[\.\;\:\-\n]+")

    def split(text: str) -> List[str]:
        parts = [p.strip() for p in splitter.split(text) if p.strip()]
        units = []
        for part in parts:
            toks = part.split()
            if len(toks) <= 12:
                units.append(part)
            else:
                for i in range(0, len(toks), 12):
                    units.append(" ".join(toks[i : i + 12]))
        return units

    return split, {"type": "InterpretiveParser", "rule": "conservative-12"}


def assemble_telos_engine(
    alpha: float = 0.5,
    beta: float = 0.3,
    gamma: float = 0.2,
) -> Tuple[Callable[[float, float, float], float], Dict[str, Any]]:
    """Telos primitive: evaluates T(c,k,e) = alpha*c + beta*k - gamma*e.

    Returns evaluate(c,k,e) -> score
    """

    def evaluate(c: float, k: float, e: float) -> float:
        t = alpha * c + beta * k - gamma * e
        return max(0.0, min(1.0, t))

    artifact = {"type": "TelosEngine", "alpha": alpha, "beta": beta, "gamma": gamma}
    return evaluate, artifact


def assemble_state_machine(
    activate_threshold: float = 0.7,
    sleep_threshold: float = 0.2,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Simple state machine descriptor (stateless factory returns descriptor and API stub).

    The returned state is a dict with methods simulated by closures.
    """
    state = {"state": "POTENTIAL", "recent_scores": []}

    def ingest(telos_score: float, validated: bool) -> None:
        recent_scores: List[float] = state["recent_scores"]
        recent_scores.append(telos_score)
        if len(recent_scores) > 20:
            recent_scores.pop(0)
        avg = sum(recent_scores) / len(recent_scores) if recent_scores else 0.0
        if state["state"] == "POTENTIAL" and avg >= activate_threshold and validated:
            state["state"] = "ACTIVE"
        elif state["state"] == "ACTIVE" and avg <= sleep_threshold:
            state["state"] = "SLEEP"
        elif state["state"] == "SLEEP" and avg >= (activate_threshold * 0.8):
            state["state"] = "POTENTIAL"

    def status() -> Dict[str, Any]:
        recent_scores: List[float] = state["recent_scores"]
        avg = sum(recent_scores) / len(recent_scores) if recent_scores else 0.0
        return {"state": state["state"], "avg_score": avg}

    artifact = {
        "type": "IntellectStateMachine",
        "activate_threshold": activate_threshold,
        "sleep_threshold": sleep_threshold,
    }
    return {"ingest": ingest, "status": status, "state_obj": state}, artifact


def assemble_abulafia_layer(
    encode_func: Callable[[str], Tuple[int, List[int], str]],
) -> Tuple[Callable[[str], Dict[str, Any]], Dict[str, Any]]:
    def abulafia_unit(unit: str) -> Dict[str, Any]:
        total, vec, sig = encode_func(unit)
        return {"unit": unit, "total": total, "vec": vec, "sig": sig}

    return abulafia_unit, {"type": "AbulafiaLayer"}


def assemble_maimonides_layer(
    validate_func: Callable[[str, str, Callable[[str], Tuple[int, List[int], str]]], bool],
    encode_func: Callable[[str], Tuple[int, List[int], str]],
) -> Tuple[Callable[[str, List[str]], Dict[str, Any]], Dict[str, Any]]:
    def validate_unit(unit: str, context: List[str]) -> Dict[str, Any]:
        checks = []
        ok = True
        for context_unit in context:
            res = validate_func(unit, context_unit, encode_func)
            checks.append({"context": context_unit, "ok": res})
            if not res:
                ok = False
        return {"unit": unit, "checks": checks, "verdict": ok}

    return validate_unit, {"type": "MaimonidesLayer"}


def build_meta_algorithm(config: Dict[str, Any] | None = None) -> Tuple[Any, List[Dict[str, Any]]]:
    """Main builder: composes primitives into the final AMNE pipeline.

    Returns (pipeline_callable, derivation_trace).

    pipeline_callable(text, context) -> result dict
    """
    cfg = config or {}
    trace = DerivationTrace()

    encode, art_enc = assemble_letter_mapper(cfg.get("weights"))
    trace.add("A:LetterMapper", "Abulafia mapping primitive assembled", art_enc)

    validate, art_val = assemble_maimonides_filter(cfg.get("theta", 0.7))
    trace.add("A:MaimonidesFilter", "Equivocation primitive assembled", art_val)

    split, art_parser = assemble_interpretive_parser()
    trace.add("A:Parser", "Interpretive parser assembled", art_parser)

    telos_eval, art_telos = assemble_telos_engine(
        cfg.get("alpha", 0.5), cfg.get("beta", 0.3), cfg.get("gamma", 0.2)
    )
    trace.add("A:Telos", "Telos primitive assembled", art_telos)

    sm, art_sm = assemble_state_machine(
        cfg.get("activate_threshold", 0.7), cfg.get("sleep_threshold", 0.2)
    )
    trace.add("A:StateMachine", "Intellect state machine assembled", art_sm)

    abula_layer, art_abula_layer = assemble_abulafia_layer(encode)
    trace.add("B:AbulafiaLayer", "Layer wrapping encode into unit API", art_abula_layer)

    maim_layer, art_maim_layer = assemble_maimonides_layer(validate, encode)
    trace.add("B:MaimonidesLayer", "Layer wrapping validation API", art_maim_layer)

    def pipeline(text: str, context: List[str]) -> Dict[str, Any]:
        units = split(text)
        unit_results = []
        telos_scores = []
        for unit in units:
            ab = abula_layer(unit)
            ma = maim_layer(unit, context)
            clarity = min(1.0, len(unit.split()) / 10.0)
            consistency = 1.0 if ma["verdict"] else 0.0
            equivocation = 0.0 if ma["verdict"] else 1.0
            score = telos_eval(clarity, consistency, equivocation)
            telos_scores.append(score)
            sm["ingest"](score, ma["verdict"])
            unit_results.append({"unit": unit, "ab": ab, "ma": ma, "score": score})
        overall = sum(telos_scores) / len(telos_scores) if telos_scores else 0.0
        status = sm["status"]()
        return {"units": unit_results, "overall_telos": overall, "intellect": status}

    trace.add(
        "C:Pipeline",
        "Pipeline composed from layers into a single callable",
        {"units": "ordered", "flow": "split->abula->maim->telos->state"},
    )

    final_artifact = {"type": "MetaAlgorithm", "id": str(uuid.uuid4())}
    trace.add("D:Finalize", "Meta-algorithm assembled into final pipeline", final_artifact)

    return pipeline, trace.dump()


if __name__ == "__main__":
    pipeline, derivation = build_meta_algorithm()
    example_text = (
        "בראשית ברא אלהים את השמים ואת הארץ. והארץ היתה תהו ובהו; וחשך על פני תהום."
    )
    res = pipeline(example_text, context=["בריאה", "אחדות", "התהוות"])
    print("DERIVATION TRACE")
    print(json.dumps(derivation, ensure_ascii=False, indent=2))
    print("\nPIPELINE RESULT")
    print(json.dumps(res, ensure_ascii=False, indent=2))
