import re


class AMNEFullCore:
    """Core epistemic processor used by the Quantum Orchestrator."""

    def process_cycle(self, instruction: str) -> dict:
        """Sanitize an instruction and produce a telos alignment score."""
        if not isinstance(instruction, str):
            raise TypeError("instruction must be a string")

        sanitized = re.sub(r"\s+", " ", instruction).strip()
        word_count = len(sanitized.split()) if sanitized else 0
        telos_score = min(1.0, word_count / 10.0)

        return {
            "sanitized_instruction": sanitized,
            "telos_score": telos_score,
        }
