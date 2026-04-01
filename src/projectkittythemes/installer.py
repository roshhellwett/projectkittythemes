import os
import json
import shutil
import sys
from pathlib import Path
from typing import Any

def get_config_path(terminal: str) -> Path | None:
    home = Path.home()
    
    if terminal == "kitty":
        config_dir = home / ".config" / "kitty"
        if sys.platform == "darwin":
            config_dir = home / ".config" / "kitty"
        elif sys.platform == "win32":
            config_dir = home / ".local" / "share" / "kitty"
        return config_dir / "kitty.conf"
    
    elif terminal == "alacritty":
        if sys.platform == "win32":
            config_dir = home / ".config" / "alacritty"
        else:
            config_dir = home / ".config" / "alacritty"
        return config_dir / "alacritty.toml"
    
    elif terminal == "wezterm":
        if sys.platform == "win32":
            config_dir = home / ".config" / "wezterm"
        else:
            config_dir = home / ".config" / "wezterm"
        return config_dir / "wezterm.lua"
    
    elif terminal == "windows-terminal":
        if sys.platform != "win32":
            return None
        appdata = os.environ.get("LOCALAPPDATA", "")
        if not appdata:
            return None
        return Path(appdata) / "Packages" / "Microsoft.WindowsTerminal_8wekyb3d8bbwe" / "LocalState" / "settings.json"
    
    return None

def get_config_dir(terminal: str) -> Path | None:
    home = Path.home()
    
    if terminal == "kitty":
        if sys.platform == "win32":
            return home / ".local" / "share" / "kitty"
        return home / ".config" / "kitty"
    
    elif terminal == "alacritty":
        if sys.platform == "win32":
            return home / ".config" / "alacritty"
        return home / ".config" / "alacritty"
    
    elif terminal == "wezterm":
        if sys.platform == "win32":
            return home / ".config" / "wezterm"
        return home / ".config" / "wezterm"
    
    elif terminal == "windows-terminal":
        if sys.platform != "win32":
            return None
        appdata = os.environ.get("LOCALAPPDATA", "")
        if not appdata:
            return None
        return Path(appdata) / "Packages" / "Microsoft.WindowsTerminal_8wekyb3d8bbwe" / "LocalState"
    
    return None

def create_backup(config_path: Path) -> Path | None:
    if config_path.exists():
        backup_path = config_path.with_suffix(config_path.suffix + ".bak")
        shutil.copy2(config_path, backup_path)
        return backup_path
    return None

def install_kitty_theme(theme: dict[str, Any]) -> bool:
    config_path = get_config_path("kitty")
    if not config_path:
        return False
    
    config_dir = config_path.parent
    config_dir.mkdir(parents=True, exist_ok=True)
    
    create_backup(config_path)
    
    from projectkittythemes.themes import get_terminal_config
    content = get_terminal_config(theme, "kitty")
    
    if content:
        with open(config_path, "w") as f:
            f.write(content)
        return True
    return False

def install_alacritty_theme(theme: dict[str, Any]) -> bool:
    config_path = get_config_path("alacritty")
    if not config_path:
        return False
    
    config_dir = config_path.parent
    config_dir.mkdir(parents=True, exist_ok=True)
    
    create_backup(config_path)
    
    from projectkittythemes.themes import get_terminal_config
    content = get_terminal_config(theme, "alacritty")
    
    if content:
        with open(config_path, "w") as f:
            f.write(content)
        return True
    return False

def install_wezterm_theme(theme: dict[str, Any]) -> bool:
    config_path = get_config_path("wezterm")
    if not config_path:
        return False
    
    config_dir = config_path.parent
    config_dir.mkdir(parents=True, exist_ok=True)
    
    create_backup(config_path)
    
    from projectkittythemes.themes import get_terminal_config
    content = get_terminal_config(theme, "wezterm")
    
    if content:
        with open(config_path, "w") as f:
            f.write(content)
        return True
    return False

def install_windows_terminal_theme(theme: dict[str, Any]) -> bool:
    config_path = get_config_path("windows-terminal")
    if not config_path:
        return False
    
    from projectkittythemes.themes import get_terminal_config
    theme_config = get_terminal_config(theme, "windows-terminal")
    
    if not theme_config:
        return False
    
    theme_data = json.loads(theme_config)
    scheme_name = theme.get("name")
    
    settings = {}
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                settings = json.load(f)
            create_backup(config_path)
        except (json.JSONDecodeError, IOError):
            settings = {}
    
    if "schemes" not in settings:
        settings["schemes"] = {}
    
    settings["schemes"][scheme_name] = theme_data
    
    config_dir = config_path.parent
    config_dir.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "w") as f:
        json.dump(settings, f, indent=2)
    
    return True


def install_theme(theme: dict[str, Any], terminal: str | None = None) -> tuple[bool, str]:
    if terminal is None:
        from projectkittythemes.themes import get_installed_terminal
        terminal = get_installed_terminal()
    
    if terminal == "kitty":
        success = install_kitty_theme(theme)
        return success, "Kitty"
    elif terminal == "alacritty":
        success = install_alacritty_theme(theme)
        return success, "Alacritty"
    elif terminal == "wezterm":
        success = install_wezterm_theme(theme)
        return success, "WezTerm"
    elif terminal == "windows-terminal":
        success = install_windows_terminal_theme(theme)
        return success, "Windows Terminal"
    
    return False, terminal

def get_install_command(theme_slug: str) -> dict[str, str]:
    base_url = "https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main"
    
    commands = {
        "bash": f"bash <(curl -s {base_url}/linux/install.sh) --theme {theme_slug}",
        "powershell": f"irm {base_url}/windows/install.ps1 | iex; Install-PKTheme -Theme {theme_slug}",
        "pip": f"pip install projectkittythemes && projectkittythemes install {theme_slug}",
    }
    
    return commands
