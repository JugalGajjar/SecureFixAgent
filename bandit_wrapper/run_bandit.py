import subprocess
import json
from typing import List, Dict

def run_bandit(file_path: str) -> List[Dict]:
    try:
        cmd = ["bandit", "-f", "json", "-q", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode not in (0, 1):  # 1 is also valid (issues found)
            print("Bandit exited with an error.")
            print("stderr:", result.stderr)
            return []

        if not result.stdout.strip():
            print("No output from Bandit. Check if the file is valid.")
            return []

        # Parse JSON output
        output = json.loads(result.stdout)
        issues = output.get("results", [])
        return issues

    except json.JSONDecodeError:
        print("Failed to parse Bandit output as JSON.")
        print("Output was:", result.stdout)
        return []

    except FileNotFoundError:
        print("Bandit not found. Make sure it's installed in your conda environment.")
        return []

    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
