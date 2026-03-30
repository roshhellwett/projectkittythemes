# Windows Installation Guide

Transform your Windows terminal with beautiful color themes in just minutes.

---

## ⚡ Quick Install

### Option 1 - Recommended (Copy & Paste)

Open **PowerShell** (not CMD) and paste this:

```powershell
irm https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/windows/install.ps1 | iex
```

### Option 2 - GUI App

1. Download `ProjectKittyThemes.exe` from this folder
2. Double-click to run
3. Follow the on-screen instructions

---

## What Terminal Do I Have?

Most Windows users have **Windows Terminal** (pre-installed on Windows 11, free from Microsoft Store on Windows 10).

Not sure? Run this in PowerShell:
```powershell
$env:TERM_PROGRAM
```

If it shows `WindowsTerminal` - you're on Windows Terminal!

---

## How to Use the Installer

### Interactive Mode (Recommended)
Just run the command - it will ask you:
1. Which terminal? (select your terminal)
2. Which theme? (choose from 7 beautiful themes)
3. Confirm? (press Y)

### Direct Install (No Questions)
Want to skip the questions? Use:

```powershell
# Windows Terminal + Tokyo Night
.\install.ps1 -Terminal windows-terminal -Theme tokyonight

# Kitty + Nord
.\install.ps1 -Terminal kitty -Theme nord
```

### Available Themes
| Theme | Look |
|-------|------|
| `tokyonight` | Blue & purple, modern |
| `catppuccin-mocha` | Purple & pink, cozy |
| `catppuccin-latte` | Light pastel |
| `gruvbox-dark` | Warm browns, retro |
| `rose-pine` | Soft pink & purple |
| `nord` | Cool blue, clean |
| `solarized-dark` | Classic, easy on eyes |

### List All Themes
```powershell
.\install.ps1 -List
```

### Preview Colors
```powershell
.\install.ps1 -Preview
```

---

## Troubleshooting

### "Script cannot be loaded"
Run PowerShell as Administrator and:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### "Theme not applying"
1. **Close Windows Terminal completely** (right-click icon → exit)
2. Open a NEW terminal window
3. Still not working? Try a different theme

### "Can't find my terminal"
Supported terminals:
- **Windows Terminal** (most common)
- **Kitty** - Download from kitty.technology
- **Alacritty** - Download from alacritty.org
- **WezTerm** - Download from wezfurlong.org

---

## Need Help?

- Website: [View all themes](https://github.com/zenithopensourceprojects/projectkittythemes)
- Issues: [Open a ticket](https://github.com/zenithopensourceprojects/projectkittythemes/issues)
