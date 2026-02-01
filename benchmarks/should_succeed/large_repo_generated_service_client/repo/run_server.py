import os
import pathlib
import json
import time
from cli.server import main

def emit_metrics_artifacts(metrics_dict, phase):
    artifacts_dir = pathlib.Path(os.environ["REMOROO_ARTIFACTS_DIR"])
    artifacts_dir.mkdir(exist_ok=True)
    targets = []
    if phase == "baseline":
        targets.append(artifacts_dir / "baseline_metrics.json")
    else:
        targets.append(artifacts_dir / "current_metrics.json")
    targets.append(artifacts_dir / "metrics.json")
    for target_file in targets:
        print(f"DEBUG: Processing target {target_file}, exists={target_file.exists()}")
        data = {}
        if target_file.exists():
            with open(target_file, "r") as f:
                data = json.load(f)
                print(f"DEBUG: Loaded keys from {target_file.name}: {list(data.get('metrics', {}).keys())}")
        if "metrics" not in data:
            data["metrics"] = {}
            data["version"] = 1
            data["phase"] = phase
            data["created_at"] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        for k, v in metrics_dict.items():
            data["metrics"][k] = v
        if phase == "baseline" and target_file.name == "metrics.json":
            if "baseline_metrics" not in data:
                data["baseline_metrics"] = {}
            for k, v in metrics_dict.items():
                data["baseline_metrics"][k] = v
        print(f"DEBUG: Writing {target_file.name} keys: {list(data['metrics'].keys())}")
        with open(target_file, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    _ = main()
    # No relevant metrics for this entrypoint, but emit empty metrics dict for completeness
    phase = os.environ.get("REMOROO_METRICS_PHASE", "current")
    metrics = {}
    emit_metrics_artifacts(metrics, phase)
    print("server complete")
