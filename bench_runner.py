import os
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import re
from metrics import BenchmarkMetrics, save_leaderboard_data

def get_latest_report_outcome(repo_path: Path):
    """
    Search for the most recent run report in .remoroo/runs/
    """
    remoroo_dir = repo_path / ".remoroo" / "runs"
    if not remoroo_dir.exists():
        return None, None

    # Get all subdirectories (run IDs) and find the most recently modified one
    run_dirs = [d for d in remoroo_dir.iterdir() if d.is_dir()]
    if not run_dirs:
        return None, None

    # Sort by modification time of the directory itself
    latest_run = max(run_dirs, key=lambda d: d.stat().st_mtime)
    report_path = latest_run / "final_report.md"

    if not report_path.exists():
        return None, None

    try:
        content = report_path.read_text()
        # Look for ## ✅ Outcome: SUCCESS or ## ❌ Outcome: FAILED
        match = re.search(r"## .* Outcome: (\w+)", content)
        if match:
            return match.group(1), str(report_path)
    except Exception:
        pass

    return None, None

def run_benchmark(case_path: Path, verbose: bool = False, skip_existing: bool = False):
    case_json_path = case_path / "case.json"
    if not case_json_path.exists():
        return None

    with open(case_json_path) as f:
        case = json.load(f)

    repo_path = case_path / case.get("repo_path", "repo")
    goal = case.get("goal")
    metrics_req = case.get("metrics")
    expected_outcome = case.get("expected_outcome", "success").upper()
    
    print(f"🚀 Processing Benchmark: {case.get('name')} ({case.get('case_id')})")

    # 1. Check for Skip Logic
    if skip_existing:
        decision, report_file = get_latest_report_outcome(repo_path)
        if decision:
            print(f"   ⏩ Skipping: Found existing report with outcome {decision}")
            return {
                "case_id": case.get("case_id"),
                "decision": decision,
                "is_correct": decision == expected_outcome,
                "skipped": True,
                "report_file": report_file
            }
    
    # 2. Construct Remoroo CLI command
    cmd = [
        "remoroo", "run",
        "--local",
        "--repo", str(repo_path),
        "--goal", goal,
        "--metrics", metrics_req,
        "--yes",
        "--no-patch"
    ]
    
    if verbose:
        print(f"Executing: {' '.join(cmd)}")

    start_time = datetime.now()
    try:
        # Use Popen to stream logs in real-time
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, # Merge stderr into stdout for easier streaming
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        full_output = []
        for line in process.stdout:
            if verbose:
                # Use end='' because line already has a newline
                print(f"   | {line}", end='')
            full_output.append(line)
        
        process.wait()
        elapsed = (datetime.now() - start_time).total_seconds()
        
        output = "".join(full_output)
        output = "".join(full_output)
        
        # New Rich-based parsing
        decision = "UNKNOWN"
        # We look for the "Run Summary" box content
        # │ SUCCESS                                                                          │
        # │ INTERRUPTED                                                                      │
        
        # Remove ANSI codes for easier regex (optional, but robust)
        clean_output = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', output)
        
        if "│ SUCCESS" in clean_output:
            decision = "SUCCESS"
        elif "│ INTERRUPTED" in clean_output or "🛑 Experiment Paused" in clean_output:
            decision = "ABORT" # Mapped to UNKNOWN or preserved as ABORT? 
            # bench_runner expects UNKNOWN for ABORT based on existing logic, but let's see.
            # Original code: if decision == "ABORT": decision = "UNKNOWN"
            # So "ABORT" -> "UNKNOWN" effectively.
        elif "│ FAILURE" in clean_output or "│ FAIL" in clean_output:
             decision = "FAIL"
             
        # Fallback to old text just in case (optional, but safe)
        if decision == "UNKNOWN":
             if "Run completed successfully" in clean_output:
                 decision = "SUCCESS"
             elif "Run finished with outcome" in clean_output:
                 for line in clean_output.splitlines():
                     if "Run finished with outcome:" in line:
                         decision = line.split(":")[-1].strip()

        if decision == "ABORT":
            decision = "UNKNOWN"
        
        
        return {
            "case_id": case.get("case_id"),
            "decision": decision,
            "is_correct": decision == expected_outcome,
            "elapsed_seconds": elapsed,
            "stdout": output,
            "stderr": "" # Stderr merged into stdout
        }

    except Exception as e:
        print(f"❌ Error executing benchmark {case.get('case_id')}: {e}")
        return {
            "case_id": case.get("case_id"),
            "decision": "ERROR",
            "is_correct": False,
            "error": str(e)
        }

def get_benchmark_name(case_id: str, bench_root: Path) -> str:
    """Get benchmark name from case.json file."""
    for case_file in bench_root.glob(f"**/{case_id}/case.json"):
        try:
            with open(case_file) as f:
                case = json.load(f)
                return case.get("name", case_id)
        except:
            pass
    return case_id

def update_readme(report: dict, readme_path: Path = Path("README.md")):
    if not readme_path.exists():
        return

    bench_root = Path("benchmarks")
    
    # Summary metrics
    summary_table = [
        "| Metric | Value |",
        "| :--- | :--- |"
    ]

    if "success_rate" in report:
        val = report["success_rate"]
        display_val = f"{val:.1f}%"
        summary_table.append(f"| **Success Rate (BSR)** | {display_val} |")
    
    if "total_runs" in report:
        summary_table.append(f"| **Total Benchmarks** | {report['total_runs']} |")

    summary_table.append(f"\n*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    # Leaderboard table
    if "raw_results" in report:
        leaderboard_table = [
            "\n## Benchmark Results",
            "",
            "| Benchmark | Status | Outcome |",
            "| :--- | :---: | :--- |"
        ]
        
        # Sort results: correct first, then by name
        results = sorted(
            report["raw_results"],
            key=lambda x: (not x.get("is_correct", False), get_benchmark_name(x.get("case_id", ""), bench_root).lower())
        )
        
        for result in results:
            case_id = result.get("case_id", "unknown")
            decision = result.get("decision", "UNKNOWN")
            is_correct = result.get("is_correct", False)
            
            benchmark_name = get_benchmark_name(case_id, bench_root)
            
            # Status emoji
            if decision == "SUCCESS":
                status_emoji = "✅"
            elif decision == "PARTIAL_SUCCESS":
                status_emoji = "⚠️"
            elif decision == "FAIL":
                status_emoji = "❌"
            else:
                status_emoji = "❓"
            
            # Outcome text
            if is_correct:
                outcome = "Correct"
            else:
                outcome = "Incorrect"
            
            leaderboard_table.append(f"| {benchmark_name} | {status_emoji} {decision} | {outcome} |")
        
        leaderboard_markdown = "\n".join(leaderboard_table)
    else:
        leaderboard_markdown = ""
    
    markdown_results = "\n".join(summary_table) + "\n" + leaderboard_markdown

    with open(readme_path, "r") as f:
        content = f.read()

    # Match the placeholder section
    pattern = r"(<!-- BENCHMARK_START -->)(.*?)(<!-- BENCHMARK_END -->)"
    new_content = re.sub(
        pattern,
        f"\\1\n{markdown_results}\n\\3",
        content,
        flags=re.DOTALL
    )

    with open(readme_path, "w") as f:
        f.write(new_content)

def main():
    parser = argparse.ArgumentParser(description="Remoroo Benchmark Runner")
    parser.add_argument("--include", type=str, default="*", help="Glob pattern to include benchmarks")
    parser.add_argument("--output", type=str, default="leaderboard.json", help="Output path for results")
    parser.add_argument("--skip-existing", action="store_true", help="Skip runs that already have a final report")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    bench_root = Path("benchmarks")
    all_results = []
    
    # Discover benchmarks
    # We look for all case.json files in subdirectories
    for case_file in bench_root.glob(f"**/{args.include}/case.json"):
        case_dir = case_file.parent
        res = run_benchmark(case_dir, verbose=args.verbose, skip_existing=args.skip_existing)
        if res:
            all_results.append(res)
            print(f"✅ Result: {res['decision']} (Correct: {res['is_correct']})")

    # Aggregate Metrics
    metrics_engine = BenchmarkMetrics(all_results)
    report = metrics_engine.generate_report()
    report["last_updated"] = datetime.now().isoformat()
    report["raw_results"] = all_results

    # Save for Website Integration
    save_leaderboard_data(report, args.output)
    
    # Update README.md with summary results
    try:
        update_readme(report)
        print("📝 README.md updated with latest results")
    except Exception as e:
        print(f"⚠️ Failed to update README.md: {e}")
    
    print("\n" + "="*40)
    print("📊 BENCHMARKING COMPLETE")
    if "success_rate" in report:
        print(f"Success Rate: {report['success_rate']:.1f}%")
    print(f"Report saved to: {args.output}")
    print("="*40)

if __name__ == "__main__":
    main()
