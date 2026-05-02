@echo off
title NetworkBuster Miner Engine
echo 🛰️ Initializing Miner (AI Training Pipeline)...
cd /d "%~dp0"
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)
python tools\python\ai-training-pipeline.py
pause
