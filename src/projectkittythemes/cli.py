import sys
import os
import json
import logging
import tempfile
from pathlib import Path
from datetime import datetime

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich.table import Table
from rich.prompt import Prompt, Confirm

from projectkittythemes import __version__
from projectkittythemes.themes import (
    get_all_themes,
    get_theme_by_slug,
    get_themes_by_category,
    get_categories,
    get_installed_terminal,
    detect_terminal,
    get_terminal_config,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = typer.Typer(help="projectkittythemes — Beautiful terminal color schemes", add_completion=False)
console = Console()

BACKUP_DIR = Path(tempfile.gettempdir()) / "projectkittythemes_backups"

TERMINAL_CONFIG_PATHS = {
    "kitty": lambda: Path.home() / ".config" / "kitty" / "kitty.conf",
    "alacritty": lambda: Path.home() / ".config" / "alacritty" / "alacritty.toml",
    "wezterm": lambda: Path.home() / ".config" / "wezterm" / "wezterm.lua",
    "windows-terminal": lambda: Path(os.environ.get("LOCALAPPDATA", "")) / "Packages" / "Microsoft.WindowsTerminal_8wekyb3d8bbwe" / "LocalState" / "settings.json",
}

SUPPORTED_TERMINALS = list(TERMINAL_CONFIG_PATHS.keys())

def get_config_path(terminal: str) -> Path | None:
    getter = TERMINAL_CONFIG_PATHS.get(terminal)
    if getter:
        return getter()
    return None

def is_interactive() -> bool:
    return sys.stdin.isatty()

def safe_input(prompt_text: str, default: str = "", allow_empty: bool = True) -> str:
    if not is_interactive():
        return default
    try:
        result = input(prompt_text).strip()
        if not result and not allow_empty:
            return default
        return result
    except (EOFError, KeyboardInterrupt):
        return ""

def pause_for_user() -> None:
    if is_interactive():
        try:
            input("\nPress Enter to continue...")
        except (EOFError, KeyboardInterrupt):
            pass

def print_version():
    console.print(f"""
[bold cyan]projectkittythemes[/bold cyan] version {__version__}

[dim]Beautiful color themes for your terminal[/dim]

[dim]--- Copyright 2026 Zenith Open Source Projects ---[/dim]
[dim]Developer: roshhellwett[/dim]
    """)

def print_error_context(message: str, context: str = "", solution: str = "") -> None:
    error_msg = f"[red]Error:[/red] {message}"
    if context:
        error_msg += f"\n[yellow]Context:[/yellow] {context}"
    if solution:
        error_msg += f"\n[green]Solution:[/green] {solution}"
    
    console.print(Panel(
        error_msg,
        title="Something went wrong",
        border_style="red",
    ))

def print_success(message: str, details: str = "") -> None:
    msg = f"[green]{message}[/green]"
    if details:
        msg += f"\n\n{details}"
    
    console.print(Panel(
        msg,
        title="Success",
        border_style="green",
    ))

def print_info(message: str, details: str = "") -> None:
    msg = f"[cyan]{message}[/cyan]"
    if details:
        msg += f"\n\n{details}"
    
    console.print(Panel(
        msg,
        title="Info",
        border_style="cyan",
    ))

def backup_current_theme(terminal: str) -> tuple[bool, str]:
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"{terminal}_backup_{timestamp}.json"
        
        config_path = get_config_path(terminal)
        if not config_path:
            return False, f"Unsupported terminal: {terminal}"
        
        backup_data = {
            "terminal": terminal,
            "timestamp": timestamp,
            "config_path": str(config_path),
        }
        
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    backup_data["config_content"] = f.read()
            except IOError as e:
                return False, f"Could not read config file: {e}"
        
        try:
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=2)
        except IOError as e:
            return False, f"Could not create backup: {e}"
        
        return True, str(backup_file)
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return False, f"Unexpected error during backup: {e}"

def restore_backup(terminal: str) -> tuple[bool, str]:
    try:
        backup_files = sorted(BACKUP_DIR.glob(f"{terminal}_backup_*.json"), reverse=True)
        
        if not backup_files:
            return False, "No backup found. Have you applied any theme before?"
        
        latest_backup = backup_files[0]
        
        try:
            with open(latest_backup, "r", encoding="utf-8") as f:
                backup_data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            return False, f"Backup file is corrupted: {e}"
        
        config_path = get_config_path(terminal)
        if not config_path:
            return False, f"Unsupported terminal: {terminal}"
        
        if "config_content" in backup_data:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with open(config_path, "w", encoding="utf-8") as f:
                    f.write(backup_data["config_content"])
            except IOError as e:
                return False, f"Could not restore config: {e}"
        
        try:
            latest_backup.unlink()
        except OSError:
            pass
        
        return True, f"Restored from backup: {backup_data.get('timestamp', 'unknown')}"
    except Exception as e:
        logger.error(f"Restore failed: {e}")
        return False, f"Unexpected error during restore: {e}"

def install_theme_to_terminal(theme: dict, terminal: str) -> tuple[bool, str]:
    try:
        slug = theme.get("slug")
        if not slug:
            return False, "Theme configuration is missing slug field"
        
        config_content = get_terminal_config(theme, terminal)
        if not config_content:
            return False, f"No configuration found for terminal '{terminal}' with theme '{theme.get('name')}'"
        
        config_path = get_config_path(terminal)
        if not config_path:
            return False, f"Terminal '{terminal}' is not supported"
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(config_content)
        except IOError as e:
            return False, f"Could not write config to {config_path}: {e}"
        
        return True, f"Theme applied to {config_path}"
    except Exception as e:
        logger.error(f"Install failed: {e}")
        return False, f"Unexpected error during installation: {e}"

def apply_theme_preview(theme: dict) -> tuple[bool, str]:
    terminal = get_installed_terminal()
    
    backup_success, backup_msg = backup_current_theme(terminal)
    if not backup_success:
        return False, f"Failed to create backup: {backup_msg}"
    
    success, install_msg = install_theme_to_terminal(theme, terminal)
    
    if not success:
        restore_backup(terminal)
        return False, install_msg
    
    return True, install_msg

def restore_default_theme() -> tuple[bool, str]:
    terminal = get_installed_terminal()
    return restore_backup(terminal)

def show_color_preview(theme: dict) -> None:
    ansi = theme.get("ansi_colors", {})
    bg = theme.get("background", "#1e1e1e")
    fg = theme.get("foreground", "#d4d4d4")
    
    console.print(f"\n[bold cyan]Theme Preview: {theme.get('name')}[/bold cyan]\n")
    
    console.print(Panel(
        Text("  Sample Text - The quick brown fox jumps over the lazy dog  ", style=Style(bgcolor=bg, color=fg)),
        title="Text Preview",
        border_style="cyan",
        subtitle=f"Background: {bg} | Foreground: {fg}",
    ))
    
    table = Table(title="ANSI Colors (Normal)", show_header=True, header_style="bold cyan")
    table.add_column("Color", style="cyan", width=12)
    table.add_column("Preview", width=24)
    table.add_column("Hex Code", style="yellow", width=12)
    
    colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    
    for color in colors:
        hex_color = ansi.get(color, "#000000")
        table.add_row(
            color.capitalize(),
            Text("        ", style=Style(bgcolor=hex_color)),
            hex_color,
        )
    
    console.print(table)
    
    bright_table = Table(title="ANSI Colors (Bright)", show_header=True, header_style="bold cyan")
    bright_table.add_column("Color", style="cyan", width=12)
    bright_table.add_column("Preview", width=24)
    bright_table.add_column("Hex Code", style="yellow", width=12)
    
    for color in colors:
        hex_color = ansi.get(f"bright_{color}", "#000000")
        bright_table.add_row(
            f"Bright {color.capitalize()}",
            Text("        ", style=Style(bgcolor=hex_color)),
            hex_color,
        )
    
    console.print(bright_table)
    
    terminals = theme.get("terminals", [])
    console.print(f"\n[dim]Supported terminals: {', '.join(terminals)}[/dim]")

def show_main_menu() -> str:
    console.clear()
    terminal = get_installed_terminal()
    terminal_display = terminal if terminal else "Unknown (not detected)"
    
    console.print(Panel(
        f"""
[bold cyan]Welcome to projectkittythemes[/bold cyan]
[dim]Beautiful color themes for your terminal[/dim]

[bold]---[/bold] [yellow]Quick Info[/yellow] [bold]---[/bold]
  Detected Terminal: {terminal_display}
  Available Themes: {len(get_all_themes())}

[bold]---[/bold] [yellow]Menu Options[/yellow] [bold]---[/bold]

  [green]1[/green]  Browse & Preview Themes
  [green]2[/green]  Apply a Theme
  [green]3[/green]  Rollback to Default Theme
  [green]4[/green]  Update projectkittythemes
  [green]5[/green]  Help & Commands
  [green]6[/green]  Exit
        """,
        title="[bold cyan]projectkittythemes Menu[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print("[dim]--- Copyright 2026 Zenith Open Source Projects | Developer: roshhellwett ---[/dim]")
    
    choice = safe_input("\n>> Enter your choice (1-6): ", allow_empty=False)
    return choice

def handle_browse_themes() -> None:
    themes = get_all_themes()
    
    if not themes:
        print_error_context(
            "No themes found!",
            "The themes directory appears to be empty",
            "Try updating the project: projectkittythemes update"
        )
        pause_for_user()
        return
    
    while True:
        console.clear()
        console.print("\n[bold cyan]--- Available Themes ---[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("#", style="dim", width=5)
        table.add_column("Theme Name", style="cyan")
        table.add_column("Category", style="yellow", width=15)
        table.add_column("Author", style="dim", width=20)
        
        for i, theme in enumerate(themes, 1):
            categories = ", ".join(theme.get("category", []))
            author = theme.get("author", "Unknown")
            table.add_row(
                f"[cyan]{i}[/cyan]",
                f"[green]{theme.get('name', 'Unknown')}[/green]",
                categories,
                author,
            )
        
        console.print(table)
        
        console.print("\n[bold]--- Actions ---[/bold]")
        console.print("  [cyan]1-{}[/cyan]  Preview and apply a theme".format(len(themes)))
        console.print("  [cyan]B[/cyan]     Go back to main menu")
        
        choice = safe_input("\n>> Enter choice: ").strip().lower()
        
        if choice == "b":
            return
        
        if not choice.isdigit():
            console.print("\n[red]Invalid input. Please enter a number or 'B'.[/red]")
            safe_input("Press Enter to continue...")
            continue
        
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(themes):
                console.print(f"\n[red]Invalid choice. Please enter a number between 1 and {len(themes)}.[/red]")
                safe_input("Press Enter to continue...")
                continue
        except ValueError:
            console.print("\n[red]Invalid input. Please enter a valid number.[/red]")
            safe_input("Press Enter to continue...")
            continue
        
        theme = themes[idx]
        show_color_preview(theme)
        
        console.print("\n[bold]--- Confirm Action ---[/bold]")
        console.print("  [green]Y[/green]  Yes, apply this theme")
        console.print("  [green]N[/green]  No, go back to theme list")
        console.print("  [green]Q[/green]  Quit to main menu")
        
        confirm = safe_input("\n>> Confirm (Y/N/Q): ", allow_empty=False).strip().lower()
        
        if confirm == "q":
            restore_default_theme()
            console.print("[dim]Theme preview cleared. Returning to main menu...[/dim]")
            safe_input("Press Enter to continue...")
            return
        elif confirm == "y":
            success, message = apply_theme_preview(theme)
            
            if success:
                print_success(
                    f"Theme '{theme.get('name')}' applied successfully!",
                    f"Terminal: {get_installed_terminal()}\n{message}\n\nPlease restart your terminal to see the changes."
                )
            else:
                print_error_context(
                    "Failed to apply theme",
                    message,
                    "Try using the rollback option or check terminal configuration"
                )
            
            safe_input("Press Enter to continue...")
            return
        else:
            continue

def handle_install_theme() -> None:
    themes = get_all_themes()
    
    if not themes:
        print_error_context(
            "No themes available",
            "The themes database is empty",
            "Update the project and try again"
        )
        pause_for_user()
        return
    
    console.clear()
    console.print("\n[bold cyan]--- Install a Theme ---[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta", box=None)
    table.add_column("#", style="dim", width=5)
    table.add_column("Theme Name", style="cyan")
    table.add_column("Category", style="yellow", width=15)
    
    for i, theme in enumerate(themes, 1):
        categories = ", ".join(theme.get("category", []))
        table.add_row(
            f"[cyan]{i}[/cyan]",
            f"[green]{theme.get('name')}[/green]",
            categories,
        )
    
    console.print(table)
    
    choice = safe_input("\n>> Enter theme number to install: ").strip()
    
    if not choice.isdigit():
        console.print("[red]Invalid choice. Returning to menu...[/red]")
        pause_for_user()
        return
    
    idx = int(choice) - 1
    if idx < 0 or idx >= len(themes):
        console.print("[red]Invalid choice. Returning to menu...[/red]")
        pause_for_user()
        return
    
    theme = themes[idx]
    terminal = get_installed_terminal()
    
    console.print(f"\n[yellow]Installing '{theme.get('name')}' to {terminal}...[/yellow]\n")
    
    success, message = install_theme_to_terminal(theme, terminal)
    
    if success:
        print_success(
            "Theme installed successfully!",
            f"Theme: {theme.get('name')}\nTerminal: {terminal}\n\nPlease restart your terminal to see the changes."
        )
    else:
        print_error_context(
            "Failed to install theme",
            message,
            "Check if your terminal configuration is valid"
        )
    
    pause_for_user()

def handle_rollback() -> None:
    console.clear()
    terminal = get_installed_terminal()
    
    console.print(f"\n[bold cyan]--- Rollback to Default Theme ---[/bold cyan]\n")
    console.print(f"[yellow]Target Terminal:[/yellow] {terminal}\n")
    
    success, message = restore_default_theme()
    
    if success:
        print_success(
            "Theme restored to default!",
            f"Restored: {message}\n\nPlease restart your terminal to see the changes."
        )
    else:
        print_info(
            "No backup found",
            f"{message}\n\nYour terminal is already using default settings."
        )
    
    console.print("\n[dim]--- Copyright 2026 Zenith Open Source Projects ---[/dim]")
    pause_for_user()

def handle_update() -> None:
    import subprocess
    
    console.clear()
    console.print("\n[bold cyan]--- Update projectkittythemes ---[/bold cyan]\n")
    console.print("[dim]Checking for updates from PyPI...[/dim]\n")
    
    try:
        result = subprocess.run(
            ["pip", "index", "versions", "projectkittythemes"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            available_versions = []
            for line in lines:
                if "Available versions:" in line:
                    available_versions = line.replace("Available versions:", "").strip().split(", ")
                    break
            
            current_result = subprocess.run(
                ["pip", "show", "projectkittythemes"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            current_version = "Unknown"
            for line in current_result.stdout.split("\n"):
                if line.startswith("Version:"):
                    current_version = line.replace("Version:", "").strip()
                    break
            
            latest_version = available_versions[-1] if available_versions else "Unknown"
            
            console.print(f"  [dim]Current version:[/dim] [yellow]{current_version}[/yellow]")
            console.print(f"  [dim]Latest version:[/dim]  [green]{latest_version}[/green]\n")
            
            if current_version != latest_version and latest_version != "Unknown":
                console.print("[bold yellow]A new version is available![/bold yellow]\n")
                
                do_update = Confirm.ask("Do you want to update now?", default=True)
                
                if do_update:
                    console.print("\n[dim]Updating package...[/dim]\n")
                    
                    update_result = subprocess.run(
                        ["pip", "install", "--upgrade", "projectkittythemes"],
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )
                    
                    if update_result.returncode == 0:
                        print_success(
                            "Update successful!",
                            "You are now running the latest version."
                        )
                    else:
                        print_error_context(
                            "Update failed",
                            update_result.stderr,
                            "Try running: pip install --upgrade projectkittythemes"
                        )
            else:
                print_info(
                    "You're up to date!",
                    f"No updates available. Current version: {current_version}"
                )
        else:
            print_error_context(
                "Could not check for updates",
                result.stderr,
                "Check your internet connection and pip installation"
            )
            
    except subprocess.TimeoutExpired:
        print_error_context(
            "Update check timed out",
            "The request took too long",
            "Check your internet connection"
        )
    except FileNotFoundError:
        print_error_context(
            "pip not found",
            "Python pip is not installed or not in PATH",
            "Ensure Python and pip are properly installed"
        )
    except Exception as e:
        logger.error(f"Update error: {e}")
        print_error_context(
            "An unexpected error occurred",
            str(e),
            "Try again later or report the issue"
        )
    
    console.print("\n[dim]--- Copyright 2026 Zenith Open Source Projects ---[/dim]")
    pause_for_user()

def handle_help() -> None:
    console.print(f"""
[bold cyan]--- Help & Commands ---[/bold cyan]

[bold yellow]Quick Commands:[/bold yellow]
  [green]projectkittythemes start[/green]         Start interactive menu mode
  [green]projectkittythemes list[/green]          List all themes
  [green]projectkittythemes install <theme>[/green] Install a theme
  [green]projectkittythemes browse[/green]        Browse themes interactively
  [green]projectkittythemes update[/green]        Check for updates
  [green]projectkittythemes rollback[/green]      Rollback to default theme
  [green]projectkittythemes --help[/green]        Show all options
  [green]projectkittythemes --version[/green]     Show version

[bold yellow]Supported Terminals:[/bold yellow]
  [cyan]- Kitty[/cyan]
  [cyan]- Alacritty[/cyan]
  [cyan]- WezTerm[/cyan]
  [cyan]- Windows Terminal[/cyan]

[bold yellow]Installation:[/bold yellow]
  [green]pip install projectkittythemes[/green]

[bold yellow]Troubleshooting:[/bold yellow]
  [dim]• If theme doesn't appear, restart your terminal[/dim]
  [dim]• Use 'rollback' if something goes wrong[/dim]
  [dim]• Run with --verbose for detailed logs[/dim]

[dim]--- Copyright 2026 Zenith Open Source Projects | Developer: roshhellwett ---[/dim]
    """)
    pause_for_user()

def main_menu_loop() -> None:
    while True:
        try:
            choice = show_main_menu()
            
            if choice == "1":
                handle_browse_themes()
            elif choice == "2":
                handle_install_theme()
            elif choice == "3":
                handle_rollback()
            elif choice == "4":
                handle_update()
            elif choice == "5":
                handle_help()
            elif choice == "6":
                console.print("\n[cyan]Thank you for using projectkittythemes![/cyan]")
                console.print("[dim]--- Copyright 2026 Zenith Open Source Projects | Developer: roshhellwett ---[/dim]\n")
                break
            else:
                console.print(f"\n[red]Invalid choice '{choice}'. Please enter a number between 1-6.[/red]")
                pause_for_user()
        except KeyboardInterrupt:
            console.print("\n\n[cyan]Goodbye! Thank you for using projectkittythemes![/cyan]")
            console.print("[dim]--- Copyright 2026 Zenith Open Source Projects | Developer: roshhellwett ---[/dim]\n")
            break
        except Exception as e:
            logger.error(f"Menu error: {e}")
            print_error_context(
                "An error occurred in the menu",
                str(e),
                "Try restarting the application"
            )
            pause_for_user()

@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-V", help="Show version and exit"),
):
    if version:
        print_version()
        raise typer.Exit()

@app.command()
def start():
    """Start interactive menu mode."""
    main_menu_loop()

@app.command()
def version():
    """Show version information."""
    print_version()

@app.command()
def update():
    """Check for updates and upgrade projectkittythemes from PyPI."""
    import subprocess
    console.print("\n[bold cyan]Checking for updates from PyPI...[/bold cyan]\n")
    
    try:
        result = subprocess.run(
            ["pip", "index", "versions", "projectkittythemes"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            available_versions = []
            for line in lines:
                if "Available versions:" in line:
                    available_versions = line.replace("Available versions:", "").strip().split(", ")
                    break
            
            current_result = subprocess.run(
                ["pip", "show", "projectkittythemes"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            current_version = "Unknown"
            for line in current_result.stdout.split("\n"):
                if line.startswith("Version:"):
                    current_version = line.replace("Version:", "").strip()
                    break
            
            latest_version = available_versions[-1] if available_versions else "Unknown"
            
            console.print(f"  Current version: [yellow]{current_version}[/yellow]")
            console.print(f"  Latest version:  [green]{latest_version}[/green]\n")
            
            if current_version != latest_version and latest_version != "Unknown":
                console.print("[bold yellow]A new version is available![/bold yellow]")
                console.print("  Updating now...\n")
                
                update_result = subprocess.run(
                    ["pip", "install", "--upgrade", "projectkittythemes"],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                
                if update_result.returncode == 0:
                    console.print("[green]Update successful![/green]\n")
                else:
                    console.print(f"[red]Update failed: {update_result.stderr}[/red]\n")
            else:
                console.print("[green]You are on the latest version![/green]\n")
        else:
            console.print("[red]Could not check for updates.[/red]\n")
            
    except Exception as e:
        console.print(f"[red]Error checking for updates: {e}[/red]\n")

@app.command()
def list(
    category: str | None = typer.Option(None, "--category", "-c", help="Filter by category"),
):
    """List all available themes."""
    if category:
        themes = get_themes_by_category(category)
    else:
        themes = get_all_themes()
    
    if not themes:
        console.print("[yellow]No themes found.[/yellow]")
        raise typer.Exit(code=1)
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Name", style="cyan")
    table.add_column("Author", style="dim")
    table.add_column("Category", style="yellow")
    
    for i, theme in enumerate(themes, 1):
        categories = ", ".join(theme.get("category", []))
        table.add_row(
            str(i),
            theme.get("name", ""),
            theme.get("author", ""),
            categories,
        )
    
    console.print(table)

@app.command()
def install(
    theme: str = typer.Argument(..., help="Theme name or slug to install"),
    terminal: str | None = typer.Option(None, "--terminal", "-t", help="Target terminal"),
):
    """Install a theme to your terminal."""
    theme_data = get_theme_by_slug(theme)
    
    if not theme_data:
        themes = get_all_themes()
        for t in themes:
            if t.get("name", "").lower() == theme.lower():
                theme_data = t
                break
    
    if not theme_data:
        console.print(f"[red]Theme '{theme}' not found.[/red]")
        console.print("[dim]Use 'projectkittythemes list' to see available themes.[/dim]")
        raise typer.Exit(code=1)
    
    if terminal is None:
        terminal = get_installed_terminal()
    
    console.print(f"\n[yellow]Installing '{theme_data.get('name')}' to {terminal}...[/yellow]")
    
    success, message = install_theme_to_terminal(theme_data, terminal)
    
    if success:
        console.print(Panel(
            f"[green]Theme installed successfully![/green]\n\n"
            f"  Theme: {theme_data.get('name')}\n"
            f"  Terminal: {terminal}\n"
            f"  Please restart your terminal.",
            title="Success",
            border_style="green",
        ))
    else:
        console.print(Panel(
            f"[red]Failed to install theme.[/red]\n\n"
            f"  Reason: {message}",
            title="Error",
            border_style="red",
        ))
        raise typer.Exit(code=1)

@app.command()
def browse():
    """Browse themes interactively."""
    handle_browse_themes()

@app.command()
def rollback():
    """Rollback to default terminal theme."""
    handle_rollback()

@app.command()
def categories():
    """View themes by category."""
    category_list = get_categories()
    
    if not category_list:
        console.print("[yellow]No categories found.[/yellow]")
        raise typer.Exit()
    
    console.print("\n[bold cyan]Theme Categories[/bold cyan]\n")
    
    for i, cat in enumerate(category_list, 1):
        themes = get_themes_by_category(cat)
        console.print(f"  [green]{i}[/green]  {cat.capitalize()} ({len(themes)} themes)")
    
    choice = safe_input("\nEnter category number (or press Enter to go back): ").strip()
    
    if not choice.isdigit():
        return
    
    idx = int(choice) - 1
    if idx < 0 or idx >= len(category_list):
        return
    
    cat = category_list[idx]
    themes = get_themes_by_category(cat)
    
    console.print(f"\n[bold cyan]{cat.capitalize()} Themes[/bold cyan]\n")
    
    table = Table(show_header=True)
    table.add_column("Name", style="cyan")
    table.add_column("Author", style="dim")
    
    for theme in themes:
        table.add_row(theme.get("name", ""), theme.get("author", ""))
    
    console.print(table)
    pause_for_user()

if __name__ == "__main__":
    app()
