import hashlib
import json
import math
from typing import Any, Dict, List, Tuple


class LetterMapper:
    """Maps Hebrew letters to numeric values and assigns a digital signature.

    Abulafia: the word becomes a vector of values (gematria + combinations).
    The implementation here is basic and can be replaced by more advanced extensions.
    """

    HEBREW_RANGE = ("\u05d0", "\u05ea")

    def __init__(self, weights: Dict[str, int] | None = None) -> None:
        self.weights = weights or {}

    def _is_hebrew(self, ch: str) -> bool:
        return LetterMapper.HEBREW_RANGE[0] <= ch <= LetterMapper.HEBREW_RANGE[1]

    def map_text(self, text: str) -> Tuple[int, List[int], str]:
        """Return (sum_value, list_of_values, signature).

        sum_value: sum of values (basis for "reality computation").
        list_of_values: vector of values per letter.
        signature: MD5 of the original text.
        """
        values: List[int] = []
        for ch in text:
            if self._is_hebrew(ch):
                base = ord(ch)
                val = base - ord(LetterMapper.HEBREW_RANGE[0]) + 1
                val += self.weights.get(ch, 0)
                values.append(val)
        total = sum(values)
        signature = hashlib.md5(text.encode("utf-8")).hexdigest()
        return total, values, signature

    def map_word_permutations_value(self, text: str, include_permutations: bool = False) -> int:
        """Optionally return a value that represents permutations of the letters.

        Currently implemented as a weighted sum of letter values and the length.
        """
        total, values, _ = self.map_text(text)
        if include_permutations:
            n = len(values)
            perm_factor = math.factorial(n) if n <= 8 else math.factorial(8)
            return total * perm_factor
        return total


class MaimonidesFilter:
    """Apply basic logical checks to reduce equivocality between concepts.

    This is an initial algorithmic version that can be expanded with more rules.
    """

    def __init__(self, equivocal_threshold: float = 0.7) -> None:
        self.equivocal_threshold = equivocal_threshold

    def is_equivocal(self, concept_a: str, concept_b: str, mapper: LetterMapper) -> bool:
        """Compare numeric signatures of two concepts to detect overlap."""
        val_a = mapper.map_text(concept_a)[0]
        val_b = mapper.map_text(concept_b)[0]
        if val_a == 0 or val_b == 0:
            return False
        ratio = min(val_a, val_b) / max(val_a, val_b)
        return ratio >= self.equivocal_threshold

    def verify_concept(self, concept: str, context: List[str], mapper: LetterMapper) -> Dict[str, Any]:
        """Run checks and return a detailed verification response."""
        results: Dict[str, Any] = {
            "concept": concept,
            "signature": mapper.map_text(concept)[2],
            "checks": [],
        }
        for ctx in context:
            eq = self.is_equivocal(concept, ctx, mapper)
            results["checks"].append({"context": ctx, "equivocal": eq})
        results["verdict"] = not any(c["equivocal"] for c in results["checks"])
        return results


class ConstellationStore:
    """Hierarchical store of sources, each constellation holds an anchor and sources."""

    def __init__(self, initial: Dict[str, Dict[str, Any]] | None = None) -> None:
        self.constellations = initial or {
            "Taurus": {"anchor": "Maimonides", "books": ["Moreh Nevukhim", "Milot HaHigayon"]},
            "Aries": {"anchor": "Tanakh", "source": "Sefaria_API"},
            "Gemini": {"anchor": "Commentators", "nodes": ["Rashi", "Ramban", "Tosafot"]},
            "Cancer": {"anchor": "Midrash", "type": "Associative_Memory"},
        }

    def get_anchor(self, name: str) -> Dict[str, Any]:
        return self.constellations.get(name, {})

    def list_constellations(self) -> List[str]:
        return list(self.constellations.keys())


class AMNEEngine:
    """Core engine containing the mapper, filter, and store."""

    def __init__(
        self,
        mapper: LetterMapper | None = None,
        logic_filter: MaimonidesFilter | None = None,
        store: ConstellationStore | None = None,
    ) -> None:
        self.mapper = mapper or LetterMapper()
        self.filter = logic_filter or MaimonidesFilter()
        self.store = store or ConstellationStore()

    def neural_fire(self, input_query: str, context: List[str] | None = None) -> Dict[str, Any]:
        context = context or []
        raw = f"Source_from_Aries: {input_query}"

        total, values, signature = self.mapper.map_text(raw)
        verification = self.filter.verify_concept(input_query, context, self.mapper)

        return {
            "input": input_query,
            "raw": raw,
            "abulafia": {
                "total": total,
                "values_len": len(values),
                "signature": signature,
            },
            "verification": verification,
            "neural_path": "Aries -> Gemini -> Taurus",
        }


if __name__ == "__main__":
    mapper = LetterMapper()
    mf = MaimonidesFilter()
    store = ConstellationStore()
    engine = AMNEEngine(mapper=mapper, logic_filter=mf, store=store)

    example = engine.neural_fire("אמת", context=["אמת הלשון", "ידע", "השגה"])
    print(json.dumps(example, ensure_ascii=False, indent=2))
