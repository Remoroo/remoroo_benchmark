import json
from pathlib import Path
from typing import List, Dict, Any, Optional

class BenchmarkMetrics:
    def __init__(self, run_results: List[Dict[str, Any]]):
        self.results = run_results
        self.total = len(run_results)

    def calculate_success_rate(self) -> Optional[float]:
        """Percentage of tasks where actual_outcome == expected_outcome. UNKNOWN is always incorrect."""
        if self.total == 0: return None
        correct_runs = sum(1 for r in self.results if r.get('is_correct', False) and r.get('decision') != 'UNKNOWN')
        return (correct_runs / self.total) * 100

    def calculate_completion_rate(self) -> Optional[float]:
        """Percentage of tasks reaching SUCCESS state, regardless of expectation. UNKNOWN excluded."""
        if self.total == 0: return None
        successes = sum(1 for r in self.results if r.get('decision') == 'SUCCESS')
        return (successes / self.total) * 100

    def calculate_healing_index(self) -> Optional[float]:
        """Recovery rate of broken environments. Returns None if no data."""
        healing_attempts = [r for r in self.results if r.get('env_shaky') is not None]
        if not healing_attempts: return None
        
        healed = sum(1 for r in healing_attempts if r.get('env_healed', False))
        return (healed / len(healing_attempts)) * 100

    def calculate_fidelity_score(self) -> Optional[float]:
        """Deterministic match rate for artifact replays. Returns None if no data."""
        fidelity_data = [r for r in self.results if 'fidelity_match' in r]
        if not fidelity_data: return None
        
        matches = sum(1 for r in fidelity_data if r['fidelity_match'])
        return (matches / len(fidelity_data)) * 100

    def get_stage_efficiency(self) -> Dict[str, Optional[float]]:
        """Average turns and time per multi-stage task."""
        turns = [r.get('turns') for r in self.results if r.get('turns') is not None]
        times = [r.get('elapsed_seconds') for r in self.results if r.get('elapsed_seconds', 0) > 0]
        
        return {
            "avg_turns": sum(turns) / len(turns) if turns else None,
            "avg_time_sec": sum(times) / len(times) if times else None
        }

    def generate_report(self) -> Dict[str, Any]:
        efficiency = self.get_stage_efficiency()
        
        raw_report = {
            "success_rate": self.calculate_success_rate(),
            "healing_index": self.calculate_healing_index(),
            "fidelity_score": self.calculate_fidelity_score(),
            "avg_turns": efficiency['avg_turns'],
            "avg_time": efficiency['avg_time_sec'],
            "total_runs": self.total
        }
        
        # Strip out metrics for which we have no data (None)
        return {k: v for k, v in raw_report.items() if v is not None}

def save_leaderboard_data(report: Dict[str, Any], output_path: str):
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=4)
