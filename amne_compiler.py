import hashlib
import json
import time
from typing import Any, Dict, List


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


class ContextResonanceMatrix:
    """מטריצת תהודה: מודדת קרבה מושגית בין טוקנים להקשר."""

    def __init__(self, mapper: AbulafiaMapper, logic_gate: MaimonidesLogicGate) -> None:
        self.mapper = mapper
        self.logic_gate = logic_gate

    def build(self, tokens: List[str], context: List[str]) -> Dict[str, Any]:
        pairs = []
        resonance_values = []

        for token in tokens:
            token_val = sum(self.mapper.encode(token))
            for ctx in context:
                ctx_val = sum(self.mapper.encode(ctx))
                resonance = self.logic_gate.check_equivocation(token_val, ctx_val)
                resonance_values.append(resonance)
                pairs.append({
                    "token": token,
                    "context": ctx,
                    "resonance": round(resonance, 4),
                })

        average = sum(resonance_values) / len(resonance_values) if resonance_values else 0.0
        strongest = max(pairs, key=lambda item: item["resonance"], default=None)

        return {
            "average": round(average, 4),
            "strongest_pair": strongest,
            "pairs": pairs,
        }


class DialecticBalancer:
    """איזון דיאלקטי: משלב תכלית, תהודה ועקביות."""

    def __init__(
        self,
        base_weight: float = 0.6,
        resonance_weight: float = 0.3,
        contradiction_penalty: float = 0.2,
    ) -> None:
        self.base_weight = base_weight
        self.resonance_weight = resonance_weight
        self.contradiction_penalty = contradiction_penalty

    def balance(self, telos_score: float, resonance: float, consistent: bool) -> Dict[str, Any]:
        score = self.base_weight * telos_score + self.resonance_weight * resonance
        if not consistent:
            score -= self.contradiction_penalty

        balanced = max(0.0, min(1.0, score))
        if balanced >= 0.8:
            state = "ASCENDING"
        elif balanced <= 0.2:
            state = "DESCENDING"
        else:
            state = "EQUILIBRIUM"

        return {
            "balanced_score": round(balanced, 4),
            "state": state,
        }


class TraceRecorder:
    """רשם עקבות: אוסף אירועים בזמן ריצה."""

    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []

    def log(self, stage: str, payload: Dict[str, Any]) -> None:
        self.events.append({
            "time": time.time(),
            "stage": stage,
            "payload": payload,
        })

    def dump(self) -> List[Dict[str, Any]]:
        return self.events


class AMNECompiler:
    """הקומפיילר המרכזי: מקבל טקסט ומייצר קוד בינארי/לוגי מוכוון תכלית."""

    def __init__(self) -> None:
        self.mapper = AbulafiaMapper()
        self.logic = MaimonidesLogicGate()
        self.telos = TelosOptimization()
        self.resonance = ContextResonanceMatrix(self.mapper, self.logic)
        self.balancer = DialecticBalancer()
        self.tracer = TraceRecorder()
        self.state = "POTENTIAL"  # שכל בכוח

    def compile(self, raw_input: str, context: List[str]) -> Dict[str, Any]:
        """תהליך הקומפילציה."""
        # 1. שלב הפירוק (Parsing)
        tokens = raw_input.split()
        encoded_tokens = [self.mapper.encode(t) for t in tokens]
        total_val = sum(sum(v) for v in encoded_tokens)
        self.tracer.log("parse", {"tokens": tokens, "total_weight": total_val})

        # 2. שלב הסינון הלוגי (Filtering)
        consistency = self.logic.is_consistent(tokens + context)
        self.tracer.log("logic_filter", {"consistent": consistency})

        # חישוב 'שם משותף' מול ההקשר
        max_equiv = 0.0
        for ctx_term in context:
            ctx_val = sum(self.mapper.encode(ctx_term))
            for t in tokens:
                t_val = sum(self.mapper.encode(t))
                max_equiv = max(max_equiv, self.logic.check_equivocation(t_val, ctx_val))

        # 3. חישוב מדדי איכות (Metrics)
        metrics = {
            "clarity": min(1.0, len(tokens) / 10.0),
            "logic": 1.0 if consistency else 0.0,
            "equivocation": max_equiv,
        }

        # 4. הפעלת מנוע התכלית
        telos_score = self.telos.compute_telos(metrics)
        self.tracer.log("telos", {"score": telos_score, "metrics": metrics})

        # 4.1 תהודה עם ההקשר
        resonance = self.resonance.build(tokens, context)
        self.tracer.log("resonance", resonance)

        # 4.2 איזון דיאלקטי
        balance = self.balancer.balance(telos_score, resonance["average"], consistency)
        self.tracer.log("balance", balance)

        # 5. עדכון מצב השכל (Transition)
        balanced_score = balance["balanced_score"]
        if balanced_score > 0.7:
            self.state = "ACTIVE"  # שכל בפועל
        elif balanced_score < 0.3:
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
                "balanced_score": balanced_score,
                "final_state": self.state,
            },
            "advanced": {
                "resonance": resonance,
                "balance": balance,
                "trace": self.tracer.dump(),
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
