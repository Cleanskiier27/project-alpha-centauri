"""
NetworkBuster Push Agent
Automates the 'One-Push' release process for the Core ecosystem.
Synchronizes Flight Kernel, AGI Host, and Audio Lab to the public distribution.
"""

import subprocess
import os
import sys
import time
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def run_cmd(cmd):
    """Run a shell command and return the output."""
    print(f"📡 Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "code": result.returncode
    }

@app.route('/api/push/sync', methods=['POST'])
def sync_core():
    print("\n" + "=" * 60)
    print(f"🚀 PUSH AGENT SYNC STARTING - {datetime.now()}")
    
    # 1. Compile public dist
    print("[1/3] Compiling public distribution...")
    comp_res = run_cmd(f"{sys.executable} public_release_manager.py")
    
    # 2. Git Status & Stage
    print("[2/3] Staging core updates...")
    run_cmd("git add .")
    run_cmd("git add public_dist/")
    status_res = run_cmd("git status --short")
    
    # 3. Commit Message Template
    commit_msg = f"Public Core Update: Flight Kernel, AGI Host, Audio Lab [{datetime.now().strftime('%Y%m%d')}]"
    
    return jsonify({
        "status": "READY_TO_DEPLOY",
        "compilation": comp_res,
        "git_status": status_res,
        "commit_suggestion": commit_msg,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({"status": "PUSH_AGENT_ACTIVE", "port": 4501})

def main():
    print("🚀 NETWORKBUSTER PUSH AGENT STARTING...")
    print("🔗 PORT: 4501")
    app.run(host='0.0.0.0', port=4501, debug=False)

if __name__ == "__main__":
    main()
