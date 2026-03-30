# Linux & macOS Installation Guide

Welcome! Choose your preferred installation method:

## Option 1: Quick Install (Recommended) 🚀

### One-Line Install
```bash
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/linux/install.sh)
```

### Interactive Mode
```bash
git clone https://github.com/zenithopensourceprojects/projectkittythemes.git
cd projectkittythemes
cd linux
bash install.sh
```

---

## Option 2: Manual Installation

### Clone the Repository
```bash
git clone https://github.com/zenithopensourceprojects/projectkittythemes.git
cd projectkittythemes
```

### Run the Install Script
```bash
bash scripts/install.sh
```

---

## Available Commands

### List All Themes
```bash
bash install.sh --list
```

### Preview Colors in Terminal
```bash
bash install.sh --preview
```

### Install a Theme
```bash
# Interactive (prompts for terminal and theme)
bash install.sh

# Direct install (no prompts)
bash install.sh --terminal kitty --theme tokyonight
```

---

## Supported Terminals (Linux/macOS)

| Terminal | Config Location | Status |
|----------|----------------|--------|
| Kitty | `~/.config/kitty/kitty.conf` | ✅ Full Support |
| Alacritty | `~/.config/alacritty/alacritty.toml` | ✅ Full Support |
| WezTerm | `~/.config/wezterm/theme.lua` | ✅ Full Support |

> **Note:** Windows Terminal configs are not supported on Linux/macOS

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

## Theme Installation Examples

### Install Tokyo Night for Kitty
```bash
bash install.sh --terminal kitty --theme tokyonight
```

### Install Nord for Alacritty
```bash
bash install.sh --terminal alacritty --theme nord
```

### Install Gruvbox for WezTerm
```bash
bash install.sh --terminal wezterm --theme gruvbox-dark
```

---

## Generate Palette SVGs

Creates visual palette images for all themes:
```bash
bash preview.sh
```

Output: `themes/*/palette.svg`

---

## Manual Installation

### Kitty
```bash
# Copy theme config
cp themes/tokyonight/kitty.conf ~/.config/kitty/

# Add to kitty.conf
echo "include kitty.conf" >> ~/.config/kitty/kitty.conf
```

### Alacritty
```bash
# Copy theme config
cp themes/tokyonight/alacritty.toml ~/.config/alacritty/
```

### WezTerm
```bash
# Copy theme config
cp themes/tokyonight/wezterm.lua ~/.config/wezterm/theme.lua
```

---

## Troubleshooting

### Permission Denied
```bash
chmod +x install.sh
```

### Theme Not Applying
1. Restart your terminal
2. Check config path is correct
3. Verify terminal supports true color

### Git Not Available
```bash
# Download as ZIP
curl -sL https://github.com/zenithopensourceprojects/projectkittythemes/archive/main.zip -o pkt.zip
unzip pkt.zip
cd pkt/main/linux
bash install.sh
```

---

## Keyboard Shortcuts (Interactive Mode)

| Key | Action |
|-----|--------|
| 1-4 | Select terminal |
| 1-4 | Select category |
| 1-7 | Select theme |
| y/n | Confirm/Cancel |

---

## Requirements

- **Bash** (or compatible shell)
- **Git** (for cloning) or **curl** (for one-liner)
- Supported terminal emulator
