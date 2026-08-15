"""
DS-RouteBench: Utility Functions
Timing, logging, file I/O, config loading.
"""
import os
import json
import time
import yaml
import logging
from pathlib import Path
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent
CONFIGS_DIR = PROJECT_ROOT / "configs"
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_ADVERSARIAL = PROJECT_ROOT / "data" / "adversarial"
RESULTS_DIR = PROJECT_ROOT / "results"
AGENTS_DIR = PROJECT_ROOT / "agents"

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
load_dotenv(PROJECT_ROOT / "environment" / ".env")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("ds_routebench")

# ---------------------------------------------------------------------------
# Config Loading
# ---------------------------------------------------------------------------
def load_yaml(filename):
    """Load a YAML config from configs/ directory."""
    path = CONFIGS_DIR / filename
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_agents_config():
    """Load agents.yaml → dict keyed by agent id."""
    raw = load_yaml("agents.yaml")
    return {a["id"]: a for a in raw["agents"]}

def load_datasets_config():
    """Load datasets.yaml → dict keyed by dataset name."""
    raw = load_yaml("datasets.yaml")
    return {d: info for d, info in raw["datasets"].items()}

def load_tasks_config():
    """Load tasks.yaml → dict keyed by task id."""
    return load_yaml("tasks.yaml")

# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------
class Timer:
    """Context manager for wall-clock timing."""
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start

def timed(func):
    """Decorator that logs execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        log.info(f"{func.__name__} completed in {elapsed:.2f}s")
        return result
    return wrapper

# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------
def save_json(data, path):
    """Save dict to JSON file, creating parent dirs."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    log.info(f"Saved: {path}")

def load_json(path):
    """Load JSON file to dict."""
    with open(path, "r") as f:
        return json.load(f)

def ensure_dir(path):
    """Create directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Result Directory
# ---------------------------------------------------------------------------
def get_result_dir(agent_id, task_id, run_id):
    """Get the output directory for a specific (agent, task, run)."""
    d = RESULTS_DIR / agent_id / task_id / f"run_{run_id}"
    d.mkdir(parents=True, exist_ok=True)
    return d

# ---------------------------------------------------------------------------
# Standard Result Dict
# ---------------------------------------------------------------------------
def make_result(agent_id, task_id, run_id=1, **kwargs):
    """Create a standardized result dictionary."""
    return {
        "agent": agent_id,
        "task_id": task_id,
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "generated_code": None,
        "predictions": None,
        "y_true": None,
        "wall_clock_sec": 0.0,
        "cost_usd": 0.0,
        "tokens_used": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "raw_output": None,
        "error": None,
        **kwargs,
    }
