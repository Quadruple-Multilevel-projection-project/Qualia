import hashlib
import json
import time
from typing import Any, Dict, List


# ---------------------------------------------------------
# AMNE COMPILER - Algorithmic Design (Final Integrated)
# ---------------------------------------------------------


class AbulafiaMapper:
    """ממפה אבולעפי: הופך אותיות לוקטורים מספריים (גימטריה אלגוריתמית)."""

    def __init__(self) -> None:
        self.ALPHABET = "אבגדהוזחטיכלמנסעפצקרשת"
        self.MAP = {char: i + 1 for i, char in enumerate(self.ALPHABET)}

    def encode(self, text: str) -> List[int]:
        return [self.MAP[c] for c in text if c in self.MAP]

    def get_signature(self, text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()[:8]


class MaimonidesLogicGate:
    """שער לוגי רמב"מי: בודק סתירות וערבוב מושגים (מילות הגיון)."""

    def __init__(self, threshold: float = 0.8) -> None:
        self.threshold = threshold
        # זוגות של הפכים לוגיים (מתוך מילות הגיון פרק ד')
        self.contradictions = [
            ("חומר", "צורה"),
            ("אפשר", "נמנע"),
            ("בכוח", "בפועל"),
            ("מקרה", "עצם"),
        ]

    def check_equivocation(self, val_a: int, val_b: int) -> float:
        """חישוב 'שם משותף' - יחס הקרבה בין ערכי המילים."""
        if val_a == 0 or val_b == 0:
            return 0.0
        return min(val_a, val_b) / max(val_a, val_b)

    def is_consistent(self, terms: List[str]) -> bool:
        """בדיקת עקביות לוגית מוחלטת."""
        for a, b in self.contradictions:
            if a in terms and b in terms:
                return False
        return True


class TelosOptimization:
    """מנוע תכלית: אופטימיזציה של ה-Objective Function (הנתיב השביעי)."""

    def __init__(self, alpha: float = 0.5, beta: float = 0.3, gamma: float = 0.2) -> None:
        self.weights = {"clarity": alpha, "logic": beta, "negation": gamma}

    def compute_telos(self, metrics: Dict[str, float]) -> float:
        """
        T = (α * Clarity) + (β * Logic) - (γ * Equivocation)
        """
        score = (
            self.weights["clarity"] * metrics.get("clarity", 0)
            + self.weights["logic"] * metrics.get("logic", 0)
            - self.weights["negation"] * metrics.get("equivocation", 0)
        )
        return max(0.0, min(1.0, score))


class AMNECompiler:
    """הקומפיילר המרכזי: מקבל טקסט ומייצר קוד בינארי/לוגי מוכוון תכלית."""

    def __init__(self) -> None:
        self.mapper = AbulafiaMapper()
        self.logic = MaimonidesLogicGate()
        self.telos = TelosOptimization()
        self.state = "POTENTIAL"  # שכל בכוח

    def compile(self, raw_input: str, context: List[str]) -> Dict[str, Any]:
        """תהליך הקומפילציה."""
        # 1. שלב הפירוק (Parsing)
        tokens = raw_input.split()
        encoded_tokens = [self.mapper.encode(t) for t in tokens]
        total_val = sum(sum(v) for v in encoded_tokens)

        # 2. שלב הסינון הלוגי (Filtering)
        consistency = self.logic.is_consistent(tokens + context)

        # חישוב 'שם משותף' מול ההקשר
        max_equiv = 0.0
        for ctx_term in context:
            ctx_val = sum(self.mapper.encode(ctx_term))
            for t in tokens:
                t_val = sum(self.mapper.encode(t))
                max_equiv = max(
                    max_equiv, self.logic.check_equivocation(t_val, ctx_val)
                )

        # 3. חישוב מדדי איכות (Metrics)
        metrics = {
            "clarity": min(1.0, len(tokens) / 10.0),
            "logic": 1.0 if consistency else 0.0,
            "equivocation": max_equiv,
        }

        # 4. הפעלת מנוע התכלית
        telos_score = self.telos.compute_telos(metrics)

        # 5. עדכון מצב השכל (Transition)
        if telos_score > 0.7:
            self.state = "ACTIVE"  # שכל בפועל
        elif telos_score < 0.3:
            self.state = "SLEEP"  # טשטוש/שינה
        else:
            self.state = "POTENTIAL"

        # תוצאת הקומפילציה
        return {
            "metadata": {
                "input": raw_input,
                "signature": self.mapper.get_signature(raw_input),
                "timestamp": time.time(),
            },
            "bytecode": {
                "op": "INTELLECT_FIRE" if self.state == "ACTIVE" else "NULL_OP",
                "values": encoded_tokens,
                "total_weight": total_val,
            },
            "validation": {
                "consistency": consistency,
                "telos_score": round(telos_score, 4),
                "final_state": self.state,
            },
        }


if __name__ == "__main__":
    compiler = AMNECompiler()

    # שאילתה לבדיקה: מושגים מופשטים
    query = "אמת והשגה מופשטת"
    context_data = ["שכל", "אור", "מציאות"]

    result = compiler.compile(query, context_data)

    print("--- AMNE COMPILER OUTPUT ---")
    print(json.dumps(result, indent=4, ensure_ascii=False))
