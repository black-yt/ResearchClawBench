"""Paths and constants for the evaluation system."""

import json
import os
from pathlib import Path

# Project root (parent of evaluation/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Tasks directory containing all benchmark tasks
TASKS_DIR = PROJECT_ROOT / "tasks"

# Workspaces directory for run outputs
WORKSPACES_DIR = PROJECT_ROOT / "workspaces"
WORKSPACES_DIR.mkdir(exist_ok=True)

# Scoring model (OpenAI-compatible; override via SCORER_MODEL env var)
SCORER_MODEL = os.environ.get("SCORER_MODEL", "gpt-5.1")

# Agent presets loaded from agents.json
# <PROMPT> and <WORKSPACE> are replaced at runtime in run_task.py
_agents_path = Path(__file__).parent / "agents.json"
try:
    with open(_agents_path, "r", encoding="utf-8") as _f:
        AGENT_PRESETS = json.load(_f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Warning: Failed to load agents.json: {e}")
    AGENT_PRESETS = {}

# Image extensions recognized for vision scoring
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"}

# Max image size for base64 encoding (10MB)
MAX_IMAGE_SIZE = 10 * 1024 * 1024
