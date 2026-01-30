import json
from pathlib import Path
from typing import Dict, Any

# defaults
APP_NAME = "rsstream"
DEFAULT_FEEDS = []

def get_config_path() -> Path:
    # standard ~/.config/rsstream location. cross-platform safe.
    config_dir = Path.home() / ".config" / APP_NAME
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"

def load_config() -> Dict[str, Any]:
    path = get_config_path()
    default_config = {
        "feeds": DEFAULT_FEEDS,
        "theme": "textual-dark", 
        "dark_mode": True
    }
    
    if not path.exists():
        return default_config
    
    try:
        with open(path, "r") as f:
            # merge defaults with what we loaded just in case keys are missing
            return {**default_config, **json.load(f)}
    except (json.JSONDecodeError, IOError):
        return default_config

def save_config(config: Dict[str, Any]):
    path = get_config_path()
    try:
        with open(path, "w") as f:
            json.dump(config, f, indent=4)
    except IOError:
        # logging goes here
        pass