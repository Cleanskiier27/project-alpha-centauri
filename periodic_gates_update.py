import os
import time
import subprocess

REPO_PATH = r"c:\Users\ceans\OneDrive\Documents\GitHub\networkbuster.net\gates"
INTERVAL = 60

def run_git_update():
    try:
        # Change to repo directory
        os.chdir(REPO_PATH)
        
        # Pull latest
        print(f"[{time.ctime()}] Pulling latest changes...")
        subprocess.run(["git", "pull"], capture_output=True)
        
        # Create a dummy update or log change
        with open("agent_status.log", "a") as f:
            f.write(f"Agent Update: {time.ctime()} - Neural Sync Complete\n")
            
        # Git add, commit, push
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Agent Auto-Update: {time.ctime()}"], capture_output=True)
        
        print(f"[{time.ctime()}] Pushing updates to origin/main...")
        subprocess.run(["git", "push"], capture_output=True)
        
        print(f"[{time.ctime()}] Synchronization finished.")
    except Exception as e:
        print(f"Error during update: {e}")

if __name__ == "__main__":
    print(f"Starting periodic updates for {REPO_PATH} every {INTERVAL} seconds...")
    while True:
        run_git_update()
        time.sleep(INTERVAL)
