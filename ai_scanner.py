import json

def scan_code():
    # Simulated AI vulnerability detection
    vulnerabilities = [
        {
            "file": "src/auth.js",
            "line": 22,
            "vulnerability": "Hardcoded Password",
            "fix": "Use environment variables to store secrets."
        },
        {
            "file": "database/queries.sql",
            "line": 34,
            "vulnerability": "SQL Injection Risk",
            "fix": "Use parameterized queries instead of string concatenation."
        }
    ]
    
    # Save results to JSON for the notifier to use
    with open("scan_results.json", "w") as f:
        json.dump(vulnerabilities, f, indent=4)

if __name__ == "__main__":
    scan_code()
