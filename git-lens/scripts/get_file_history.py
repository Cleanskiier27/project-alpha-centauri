#!/usr/bin/env python3
import subprocess
import sys
import json

def get_file_history(file_path, limit=10):
    try:
        cmd = ["git", "log", "-n", str(limit), "--pretty=format:%H|%an|%ad|%s", "--date=short", "--", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        history = []
        for line in result.stdout.strip().split('\n'):
            if not line: continue
            parts = line.split('|')
            history.append({
                "hash": parts[0],
                "author": parts[1],
                "date": parts[2],
                "subject": parts[3]
            })
        return history
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_file_history.py <file_path> [limit]")
        sys.exit(1)
    
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    print(json.dumps(get_file_history(path, limit), indent=2))
