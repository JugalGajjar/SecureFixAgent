from run_bandit import run_bandit

issues = run_bandit("data/test_vuln.py")

if not issues:
    print("No issues returned.")
else:
    print("Issues found:")
    for issue in issues:
        print(f"- {issue['line_number']}: {issue['issue_text']} [{issue['test_id']}] ({issue['issue_severity']})")
