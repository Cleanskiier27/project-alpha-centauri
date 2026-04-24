"""
NetworkBuster Public Release Manager
Compiles a distribution-ready public repository with integrated streaming.
"""

import os
import shutil
import json
from pathlib import Path

# Files to include in the public distribution
PUBLIC_MANIFEST = [
    "server-universal.js",
    "server-audio.js",
    "music-factory.js",
    "music-studio.html",
    "agi_music_video_host.py",
    "agi_cinematic_overlay.html",
    "public-landing.html",
    "index.html",
    "package.json",
    "Dockerfile",
    "docker-compose.yml",
    "README.md",
    "AUDIO-STREAMING-GUIDE.md",
    "AEROSPACE_GALAXY_NAVIGATION.md"
]

def compile_public_repo(output_dir="public_dist"):
    print(f"🚀 COMPILING PUBLIC REPOSITORY: {output_dir}")
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # Copy manifest files
    for item in PUBLIC_MANIFEST:
        if os.path.exists(item):
            print(f"   + Adding {item}")
            if os.path.isdir(item):
                shutil.copytree(item, os.path.join(output_dir, item))
            else:
                shutil.copy2(item, os.path.join(output_dir, item))
        else:
            print(f"   ! Warning: {item} not found")

    # Create dummy .env for public use
    with open(os.path.join(output_dir, ".env.example"), "w") as f:
        f.write("PORT=3000\nAUDIO_PORT=3002\nAGI_PORT=4500\nNODE_ENV=production\n")

    print(f"\n✅ PUBLIC REPOSITORY COMPILED SUCCESSFULLY IN: {output_dir}")
    print("📦 Ready for release: Includes MP3/MP4 stream hooks.")

if __name__ == "__main__":
    compile_public_repo()
