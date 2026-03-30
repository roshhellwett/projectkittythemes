# Windows Installation Guide

Welcome, Windows user! Choose your preferred installation method:

## Option 1: GUI Application (Recommended) 🎯

### ProjectKittyThemes Manager
A simple, user-friendly application to install and manage themes.

**Download:** `ProjectKittyThemes-Manager.exe`

1. Double-click `ProjectKittyThemes-Manager.exe` to run
2. Press **ENTER** to start
3. Select **1** to install a theme
4. Navigate with **↑/↓** arrows
5. Press **I** to install, **Y** to confirm
6. Restart your terminal!

### Features
- Auto-detects your installed terminal
- Creates backup before changes
- Easy theme preview
- One-click removal

---

## Option 2: PowerShell Script

### Quick Install
```powershell
irm https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/windows/install.ps1 | iex
```

### Interactive Mode
1. Open PowerShell
2. Run: `.\install.ps1`
3. Select terminal and theme
4. Restart terminal

### Install with Flags
```powershell
.\install.ps1 -Terminal windows-terminal -Theme tokyonight
```

### Available Flags
| Flag | Description | Values |
|------|-------------|--------|
| `-Terminal` | Target terminal | `windows-terminal`, `kitty` |
| `-Theme` | Theme to install | `tokyonight`, `nord`, etc. |
| `-List` | Show all themes | - |
| `-Preview` | Preview colors | - |

---

## Supported Terminals (Windows)

| Terminal | Path | Status |
|----------|------|--------|
| Windows Terminal | `%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_...` | ✅ Full Support |
| Kitty | `%APPDATA%\kitty\kitty.conf` | ✅ Full Support |
| Alacritty | `%APPDATA%\alacritty\alacritty.toml` | ✅ Full Support |
| WezTerm | `%USERPROFILE%\.wezterm.lua` | ✅ Full Support |

---

## Available Themes

| Theme | Category | Description |
|-------|----------|-------------|
| Tokyo Night | Dark | Blue-toned, neon accents |
| Catppuccin Mocha | Dark | Purple-toned, warm pinks |
| Catppuccin Latte | Pastel | Light mode, soft pastels |
| Gruvbox Dark | Dark | Warm, retro aesthetic |
| Rose Pine | Pastel | Soft pinks and purples |
| Nord | High-Contrast | Arctic blues, cold tones |
| Solarized Dark | High-Contrast | Classic, low-blue light |

---

## Troubleshooting

### "Execution Policy" Error
If PowerShell blocks the script, run:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Terminal Not Detected
Make sure your terminal is installed:
- **Windows Terminal**: Microsoft Store
- **Kitty**: https://kitty.technology
- **Alacritty**: https://alacritty.org
- **WezTerm**: https://wezfurlong.org/wezterm

### Theme Not Applying
1. Restart your terminal completely
2. Make sure only one theme is active
3. Check if terminal supports true color

---

## Keyboard Shortcuts (GUI App)

| Key | Action |
|-----|--------|
| 1 | Install theme |
| 2 | Remove theme |
| 3 | Preview all |
| ↑/↓ | Navigate |
| I | Install |
| R | Remove |
| Y/N | Confirm/Cancel |
| Q | Quit |
