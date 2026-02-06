import json
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class NNNReceptor:
    name: str
    provider: str

    def run(self) -> None:
        print(f"🔗 [NNN] {self.name} ({self.provider}) receiving orchestration signal...")
        time.sleep(0.1)
        print(f"✅ [NNN] {self.name} synchronized.")


class MultiAccountSovereignEngine:
    def __init__(self, config_path: str) -> None:
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        self.config = json.loads(config_file.read_text(encoding="utf-8"))
        self.accounts: Dict[str, NNNReceptor] = {}

    def add_account(self, name: str, provider: str) -> None:
        self.accounts[name] = NNNReceptor(name=name, provider=provider)
        print(f"➕ [ENGINE] Added account {name} via {provider}.")

    def run_bridged_deployment(self) -> None:
        threads: List[threading.Thread] = []
        print("🚀 [ENGINE] Launching bridged deployment across accounts...")

        for receptor in self.accounts.values():
            thread = threading.Thread(target=receptor.run, daemon=True)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        print("🌐 [ENGINE] Deployment complete.")
