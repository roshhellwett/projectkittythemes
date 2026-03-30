# PROJECT KITTY THEMES

[![Themes](https://img.shields.io/badge/7-Themes-ff6b6b?style=flat-square)](themes)
[![Terminals](https://img.shields.io/badge/4-Terminals-4ecdc4?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-45b7d1?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/zenithopensourceprojects/projectkittythemes?style=flat-square)]()

A curated collection of beautiful, carefully crafted terminal color schemes for Kitty, Alacritty, WezTerm, and Windows Terminal.

---

## Choose Your Platform

### For Windows Users
📁 **[Go to `windows/` folder](windows/)** - Download `.exe` or use PowerShell script

### For Linux / macOS Users  
📁 **[Go to `linux/` folder](linux/)** - Use Bash script

---

## Quick Start

### Windows
```powershell
# Option 1: Download and run the GUI app
# → windows/ProjectKittyThemes-Manager.exe

# Option 2: PowerShell one-liner
irm https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/windows/install.ps1 | iex
```

### Linux / macOS
```bash
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/linux/install.sh)
```

---

## Theme Gallery

| Theme | Category | Kitty | Alacritty | WezTerm | Windows Terminal |
|-------|----------|:-----:|:---------:|:-------:|:----------------:|
| Tokyo Night | Dark | ✅ | ✅ | ✅ | ✅ |
| Catppuccin Mocha | Dark | ✅ | ✅ | ✅ | ✅ |
| Catppuccin Latte | Pastel | ✅ | ✅ | ✅ | ✅ |
| Gruvbox Dark | Dark | ✅ | ✅ | ✅ | ✅ |
| Rosé Pine | Pastel | ✅ | ✅ | ✅ | ✅ |
| Nord | High-Contrast | ✅ | ✅ | ✅ | ✅ |
| Solarized Dark | High-Contrast | ✅ | ✅ | ✅ | ✅ |

---

## Available Themes

### 🌙 Dark Themes
- **Tokyo Night** - Blue-toned with neon accents, by enkia
- **Catppuccin Mocha** - Purple-toned with warm pinks, by Catppuccin
- **Gruvbox Dark** - Warm retro aesthetic, by morhetz

### 🌸 Pastel Themes
- **Catppuccin Latte** - Light mode with soft pastels, by Catppuccin
- **Rosé Pine** - Soft pinks and purples, by Rosé Pine

### 🔆 High-Contrast Themes
- **Nord** - Arctic blues and cold tones, by arcticicestudio
- **Solarized Dark** - Classic low-blue light design, by altercation

---

## Project Structure

```
projectkittythemes/
├── windows/                    ← Windows users start here!
│   ├── ProjectKittyThemes-Manager.exe
│   ├── install.ps1
│   ├── README.md
│   └── theme-manager/
│
├── linux/                      ← Linux/Mac users start here!
│   ├── install.sh
│   ├── preview.sh
│   └── README.md
│
├── themes/                     ← All theme files (cross-platform)
│   ├── tokyonight/
│   ├── catppuccin-mocha/
│   ├── catppuccin-latte/
│   ├── gruvbox-dark/
│   ├── rose-pine/
│   ├── nord/
│   └── solarized-dark/
│
├── web/                        ← Web gallery preview
│   └── index.html
│
├── categories/                 ← Theme categories
├── README.md                   ← You are here
├── CONTRIBUTING.md             ← How to contribute
└── THEMES.md                   ← Detailed theme info
```

---
