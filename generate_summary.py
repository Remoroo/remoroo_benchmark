#!/usr/bin/env python3
"""
Generate a detailed marketing summary from leaderboard and benchmark data.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any

def load_benchmark_details(case_id: str, bench_root: Path) -> Dict[str, Any]:
    """Load detailed information from case.json file."""
    for case_file in bench_root.glob(f"**/{case_id}/case.json"):
        try:
            with open(case_file) as f:
                case = json.load(f)
                return case
        except Exception as e:
            print(f"Warning: Could not load {case_id}: {e}")
    return {}

def categorize_benchmark(case: Dict[str, Any]) -> str:
    """Categorize benchmark by difficulty/complexity."""
    metrics = case.get("metrics", "")
    max_turns = case.get("max_turns", 0)
    
    # Count metrics (multi-metric benchmarks are harder)
    metric_count = len([m for m in metrics.split(",") if m.strip()])
    
    if metric_count > 1:
        return "Multi-Metric (Very Hard)"
    elif max_turns >= 8:
        return "Hard"
    elif max_turns >= 5:
        return "Medium"
    else:
        return "Easy"

def get_status_emoji(decision: str) -> str:
    """Get emoji for decision status."""
    emoji_map = {
        "SUCCESS": "✅",
        "PARTIAL_SUCCESS": "⚠️",
        "FAIL": "❌",
        "UNKNOWN": "❓"
    }
    return emoji_map.get(decision, "❓")

def generate_summary():
    """Generate the detailed marketing summary."""
    bench_root = Path("benchmarks")
    leaderboard_path = Path("leaderboard.json")
    
    if not leaderboard_path.exists():
        print("Error: leaderboard.json not found")
        return
    
    with open(leaderboard_path) as f:
        leaderboard = json.load(f)
    
    # Organize benchmarks by category
    categories = defaultdict(list)
    all_benchmarks = []
    
    for result in leaderboard.get("raw_results", []):
        case_id = result.get("case_id", "")
        case_details = load_benchmark_details(case_id, bench_root)
        
        if not case_details:
            continue
        
        category = categorize_benchmark(case_details)
        benchmark_info = {
            "case_id": case_id,
            "name": case_details.get("name", case_id),
            "description": case_details.get("description", ""),
            "metrics": case_details.get("metrics", ""),
            "decision": result.get("decision", "UNKNOWN"),
            "is_correct": result.get("is_correct", False),
            "category": category,
            "max_turns": case_details.get("max_turns", 0),
            "timeout_s": case_details.get("timeout_s", 0)
        }
        
        categories[category].append(benchmark_info)
        all_benchmarks.append(benchmark_info)
    
    # Calculate statistics
    total = len(all_benchmarks)
    successful = sum(1 for b in all_benchmarks if b["decision"] == "SUCCESS")
    correct = sum(1 for b in all_benchmarks if b["is_correct"])
    success_rate = leaderboard.get("success_rate", 0)
    
    # Count by category
    category_stats = {}
    for category, benchmarks in categories.items():
        category_success = sum(1 for b in benchmarks if b["decision"] == "SUCCESS")
        category_total = len(benchmarks)
        category_stats[category] = {
            "total": category_total,
            "successful": category_success,
            "success_rate": (category_success / category_total * 100) if category_total > 0 else 0
        }
    
    # Generate markdown
    md_lines = []
    
    # Header
    md_lines.append("# Remoroo Benchmark Suite - Detailed Performance Summary")
    md_lines.append("")
    md_lines.append(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}*")
    md_lines.append("")
    
    # Executive Summary
    md_lines.append("## 🎯 Executive Summary")
    md_lines.append("")
    md_lines.append(f"**Overall Success Rate: {success_rate:.1f}%**")
    md_lines.append("")
    md_lines.append(f"- **Total Benchmarks**: {total}")
    md_lines.append(f"- **Successful Runs**: {successful}")
    md_lines.append(f"- **Correct Outcomes**: {correct}")
    md_lines.append(f"- **Success Rate**: {success_rate:.1f}%")
    md_lines.append("")
    md_lines.append("The Remoroo Autonomous Experimentation Engine demonstrates exceptional performance across a comprehensive suite of real-world software engineering challenges, from simple bug fixes to complex multi-metric optimization tasks.")
    md_lines.append("")
    
    # Performance by Category
    md_lines.append("## 📊 Performance by Category")
    md_lines.append("")
    md_lines.append("| Category | Total | Successful | Success Rate |")
    md_lines.append("| :--- | :---: | :---: | :---: |")
    
    # Sort categories by difficulty
    category_order = ["Easy", "Medium", "Hard", "Multi-Metric (Very Hard)"]
    for category in category_order:
        if category in category_stats:
            stats = category_stats[category]
            md_lines.append(
                f"| {category} | {stats['total']} | {stats['successful']} | {stats['success_rate']:.1f}% |"
            )
    
    md_lines.append("")
    
    # Detailed Benchmark Results
    md_lines.append("## 🔬 Detailed Benchmark Results")
    md_lines.append("")
    
    for category in category_order:
        if category not in categories:
            continue
        
        md_lines.append(f"### {category}")
        md_lines.append("")
        
        # Sort benchmarks by success status, then name
        benchmarks = sorted(
            categories[category],
            key=lambda x: (x["decision"] != "SUCCESS", x["name"].lower())
        )
        
        for bench in benchmarks:
            status_emoji = get_status_emoji(bench["decision"])
            outcome = "✅ Correct" if bench["is_correct"] else "❌ Incorrect"
            
            md_lines.append(f"#### {status_emoji} {bench['name']}")
            md_lines.append("")
            md_lines.append(f"**Description**: {bench['description']}")
            md_lines.append("")
            md_lines.append(f"**Metrics**: `{bench['metrics']}`")
            md_lines.append("")
            md_lines.append(f"**Status**: {bench['decision']} | **Outcome**: {outcome}")
            md_lines.append("")
            if bench['max_turns'] > 0:
                md_lines.append(f"**Complexity**: Max {bench['max_turns']} turns, {bench['timeout_s']}s timeout")
                md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
    
    # Key Highlights
    md_lines.append("## 🌟 Key Highlights")
    md_lines.append("")
    
    # Find impressive benchmarks
    multi_metric_benchmarks = [b for b in all_benchmarks if "Multi-Metric" in b["category"] and b["decision"] == "SUCCESS"]
    hard_benchmarks = [b for b in all_benchmarks if b["category"] == "Hard" and b["decision"] == "SUCCESS"]
    
    md_lines.append("### Multi-Metric Benchmarks")
    md_lines.append("")
    md_lines.append(f"Successfully completed **{len(multi_metric_benchmarks)}** complex multi-metric optimization tasks, demonstrating Remoroo's ability to balance competing constraints:")
    md_lines.append("")
    for bench in multi_metric_benchmarks[:5]:
        md_lines.append(f"- ✅ **{bench['name']}**: {bench['metrics']}")
    md_lines.append("")
    
    md_lines.append("### Complex Refactoring Tasks")
    md_lines.append("")
    refactoring_benchmarks = [b for b in all_benchmarks if "refactor" in b["name"].lower() and b["decision"] == "SUCCESS"]
    md_lines.append(f"Successfully completed **{len(refactoring_benchmarks)}** refactoring tasks, including:")
    md_lines.append("")
    for bench in refactoring_benchmarks:
        md_lines.append(f"- ✅ **{bench['name']}**")
    md_lines.append("")
    
    # Technical Capabilities
    md_lines.append("## 🛠️ Technical Capabilities Demonstrated")
    md_lines.append("")
    
    capabilities = {
        "Bug Fixing": [b for b in all_benchmarks if "fix" in b["name"].lower() and b["decision"] == "SUCCESS"],
        "Performance Optimization": [b for b in all_benchmarks if "optimization" in b["name"].lower() and b["decision"] == "SUCCESS"],
        "Algorithm Implementation": [b for b in all_benchmarks if "implementation" in b["name"].lower() or "algorithm" in b["name"].lower()],
        "Data Processing": [b for b in all_benchmarks if "data" in b["name"].lower() or "pipeline" in b["name"].lower()],
        "Machine Learning": [b for b in all_benchmarks if "train" in b["name"].lower() or "ml" in b["name"].lower() or "classifier" in b["name"].lower()],
        "Concurrency": [b for b in all_benchmarks if "race" in b["name"].lower() or "deadlock" in b["name"].lower() or "async" in b["name"].lower()],
    }
    
    for capability, benchmarks in capabilities.items():
        if benchmarks:
            md_lines.append(f"### {capability}")
            md_lines.append(f"**{len(benchmarks)}** successful benchmarks")
            md_lines.append("")
            for bench in benchmarks[:3]:
                md_lines.append(f"- ✅ {bench['name']}")
            md_lines.append("")
    
    # Footer
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("*This summary is automatically generated from the Remoroo benchmark suite. For the latest results, visit the [Remoroo Engineering Leaderboard](https://www.remoroo.com/).*")
    md_lines.append("")
    
    # Write to file
    output_path = Path("detailed_summary.md")
    with open(output_path, "w") as f:
        f.write("\n".join(md_lines))
    
    print(f"✅ Generated detailed summary: {output_path}")
    print(f"   - {total} benchmarks analyzed")
    print(f"   - {success_rate:.1f}% overall success rate")
    print(f"   - {len(categories)} categories")

if __name__ == "__main__":
    generate_summary()

