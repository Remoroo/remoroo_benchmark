import os
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from metrics import BenchmarkMetrics, save_leaderboard_data

def run_benchmark(case_path: Path, verbose: bool = False):
    case_json_path = case_path / "case.json"
    if not case_json_path.exists():
        return None

    with open(case_json_path) as f:
        case = json.load(f)

    repo_path = case_path / case.get("repo_path", "repo")
    goal = case.get("goal")
    metrics_req = case.get("metrics")
    
    print(f"🚀 Running Benchmark: {case.get('name')} ({case.get('case_id')})")
    
    # Construct Remoroo CLI command
    # We use --yes to skip confirmation and --local for offline execution
    cmd = [
        "remoroo", "run",
        "--local",
        "--repo", str(repo_path),
        "--goal", goal,
        "--metrics", metrics_req,
        "--yes"
    ]
    
    if verbose:
        print(f"Executing: {' '.join(cmd)}")

    start_time = datetime.now()
    try:
        # Run the command and capture output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # Parse decision from output (assuming CLI prints "Run outcome: SUCCESS" or similar)
        # In a real scenario, we might read from .remoroo/runs/<run_id>/metadata.json
        # For this runner, we'll try to find the run_id in the output to locate the metadata
        
        output = result.stdout + result.stderr
        decision = "UNKNOWN"
        if "Run completed successfully" in output:
            decision = "SUCCESS"
        elif "Run finished with outcome" in output:
            # Try to grab the outcome like "Run finished with outcome: FAILED"
            for line in output.splitlines():
                if "Run finished with outcome:" in line:
                    decision = line.split(":")[-1].strip()
        
        return {
            "case_id": case.get("case_id"),
            "decision": decision,
            "elapsed_seconds": elapsed,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        print(f"❌ Error executing benchmark {case.get('case_id')}: {e}")
        return {
            "case_id": case.get("case_id"),
            "decision": "ERROR",
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="Remoroo Benchmark Runner")
    parser.add_argument("--include", type=str, default="*", help="Glob pattern to include benchmarks")
    parser.add_argument("--output", type=str, default="leaderboard.json", help="Output path for results")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    bench_root = Path("benchmarks")
    all_results = []
    
    # Discover benchmarks
    # We look for all case.json files in subdirectories
    for case_file in bench_root.glob(f"**/{args.include}/case.json"):
        case_dir = case_file.parent
        res = run_benchmark(case_dir, verbose=args.verbose)
        if res:
            all_results.append(res)
            print(f"✅ Result: {res['decision']} ({res['elapsed_seconds']:.2f}s)")

    # Aggregate Metrics
    metrics_engine = BenchmarkMetrics(all_results)
    report = metrics_engine.generate_report()
    report["last_updated"] = datetime.now().isoformat()
    report["raw_results"] = all_results

    # Save for Website Integration
    save_leaderboard_data(report, args.output)
    
    print("\n" + "="*40)
    print("📊 BENCHMARKING COMPLETE")
    print(f"Success Rate: {report['success_rate']:.1f}%")
    print(f"Env Healing Index: {report['healing_index']:.1f}%")
    print(f"Report saved to: {args.output}")
    print("="*40)

if __name__ == "__main__":
    main()
