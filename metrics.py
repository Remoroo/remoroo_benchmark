import json
from pathlib import Path
from typing import List, Dict, Any

class BenchmarkMetrics:
    def __init__(self, run_results: List[Dict[str, Any]]):
        self.results = run_results
        self.total = len(run_results)

    def calculate_success_rate(self) -> float:
        """Percentage of tasks reaching SUCCESS state."""
        if self.total == 0: return 0.0
        successes = sum(1 for r in self.results if r.get('decision') == 'SUCCESS')
        return (successes / self.total) * 100

    def calculate_healing_index(self) -> float:
        """Recovery rate of broken environments."""
        healing_attempts = [r for r in self.results if r.get('env_shaky', False)]
        if not healing_attempts: return 100.0 # No shaky envs found
        
        healed = sum(1 for r in healing_attempts if r.get('env_healed', False))
        return (healed / len(healing_attempts)) * 100

    def calculate_fidelity_score(self) -> float:
        """Deterministic match rate for artifact replays."""
        fidelity_data = [r for r in self.results if 'fidelity_match' in r]
        if not fidelity_data: return 0.0
        
        matches = sum(1 for r in fidelity_data if r['fidelity_match'])
        return (matches / len(fidelity_data)) * 100

    def get_stage_efficiency(self) -> Dict[str, float]:
        """Average turns and time per multi-stage task."""
        turns = [r.get('turns', 0) for r in self.results if r.get('turns', 0) > 0]
        times = [r.get('elapsed_seconds', 0) for r in self.results if r.get('elapsed_seconds', 0) > 0]
        
        return {
            "avg_turns": sum(turns) / len(turns) if turns else 0,
            "avg_time_sec": sum(times) / len(times) if times else 0
        }

    def generate_report(self) -> Dict[str, Any]:
        efficiency = self.get_stage_efficiency()
        return {
            "success_rate": self.calculate_success_rate(),
            "healing_index": self.calculate_healing_index(),
            "fidelity_score": self.calculate_fidelity_score(),
            "avg_turns": efficiency['avg_turns'],
            "avg_time": efficiency['avg_time_sec'],
            "total_runs": self.total
        }

def save_leaderboard_data(report: Dict[str, Any], output_path: str):
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=4)
