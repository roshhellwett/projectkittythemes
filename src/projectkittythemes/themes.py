import json
import os
from pathlib import Path
from typing import Any
from functools import lru_cache

_THEMES_DIR = Path(__file__).parent / "themes"

@lru_cache(maxsize=1)
def get_themes_dir() -> Path:
    return _THEMES_DIR

@lru_cache(maxsize=1)
def get_all_themes() -> list[dict[str, Any]]:
    themes = []
    if not _THEMES_DIR.exists():
        return themes
    
    for theme_dir in _THEMES_DIR.iterdir():
        if theme_dir.is_dir():
            theme_json = theme_dir / "theme.json"
            if theme_json.exists():
                with open(theme_json, "r") as f:
                    themes.append(json.load(f))
    
    return sorted(themes, key=lambda x: x.get("name", ""))

@lru_cache(maxsize=1)
def get_theme_by_slug(slug: str) -> dict[str, Any] | None:
    themes = get_all_themes()
    for theme in themes:
        if theme.get("slug") == slug:
            return theme
    return None

@lru_cache(maxsize=1)
def get_themes_by_category(category: str) -> list[dict[str, Any]]:
    themes = get_all_themes()
    return [t for t in themes if category in t.get("category", [])]

@lru_cache(maxsize=1)
def get_categories() -> list[str]:
    categories = set()
    for theme in get_all_themes():
        categories.update(theme.get("category", []))
    return sorted(categories)

def detect_terminal() -> str | None:
    import platform
    
    system = platform.system()
    
    if system == "Windows":
        wt = os.environ.get("WT_SESSION")
        if wt:
            return "windows-terminal"
        return "windows-terminal"
    
    term = os.environ.get("TERM", "").lower()
    if "kitty" in term:
        return "kitty"
    if "alacritty" in term:
        return "alacritty"
    if "wezterm" in term or "wez" in term:
        return "wezterm"
    
    if system == "Darwin":
        term_program = os.environ.get("TERM_PROGRAM", "").lower()
        if "kitty" in term_program:
            return "kitty"
        if "wezterm" in term_program:
            return "wezterm"
        if "alacritty" in term_program:
            return "alacritty"
    
    return None

def get_installed_terminal() -> str:
    detected = detect_terminal()
    if detected:
        return detected
    
    import platform
    if platform.system() == "Windows":
        return "windows-terminal"
    
    return "kitty"

def get_terminal_config(theme: dict[str, Any], terminal: str) -> str | None:
    slug = theme.get("slug")
    if not slug:
        return None
    
    config_dir = _THEMES_DIR / slug
    if not config_dir.exists():
        return None
    
    config_files = {
        "kitty": "kitty.conf",
        "alacritty": "alacritty.toml",
        "wezterm": "wezterm.lua",
        "windows-terminal": "windows-terminal.json",
    }
    
    config_file = config_dir / config_files.get(terminal, "")
    if config_file.exists():
        with open(config_file, "r") as f:
            return f.read()
    
    return None
