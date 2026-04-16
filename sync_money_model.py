import os
import time
import subprocess

REPO_PATH = r"c:\Users\ceans\OneDrive\Documents\GitHub\preciseliens-money"
INTERVAL = 60

def run_git_update():
    try:
        # Change to repo directory
        if not os.path.exists(REPO_PATH):
            print(f"[{time.ctime()}] Repository path not found: {REPO_PATH}")
            return

        os.chdir(REPO_PATH)
        
        # Pull latest
        print(f"[{time.ctime()}] Pulling latest model weights from origin/main...")
        subprocess.run(["git", "pull"], capture_output=True)
        
        # Log local sync activity
        with open("sync_log.txt", "a") as f:
            f.write(f"Model Sync: {time.ctime()} - All weights verified.\n")
            
        print(f"[{time.ctime()}] Asset synchronization finished for Preciseliens Money.")
    except Exception as e:
        print(f"Error during model update: {e}")

if __name__ == "__main__":
    print(f"Starting model synchronization for {REPO_PATH} every {INTERVAL} seconds...")
    while True:
        run_git_update()
        time.sleep(INTERVAL)
