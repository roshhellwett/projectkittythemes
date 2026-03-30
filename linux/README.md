# Linux & macOS Installation Guide

Transform your terminal with beautiful color themes in just minutes.

---

## ⚡ Quick Install

Open your terminal (bash/zsh) and paste this:

```bash
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/linux/install.sh)
```

That's it! Follow the simple prompts to select your terminal and theme.

---

## What Terminal Do I Have?

Not sure? Run this:

```bash
echo $TERM_PROGRAM
```

Common results:
- `Apple_Terminal` → macOS Terminal
- `iTerm.app` → iTerm2
- `vscode` → VS Code Terminal
- `kitty` → Kitty
- `wezterm` → WezTerm

---

## How to Use

### Interactive Mode (Recommended)
1. Run the install command
2. Select your terminal (1-4)
3. Select theme category (1-4)
4. Choose a theme (1-7)
5. Confirm with Y

### Direct Install (No Questions)
```bash
# Install Tokyo Night for Kitty
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/linux/install.sh) --terminal kitty --theme tokyonight

# Install Nord for Alacritty
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/linux/install.sh) --terminal alacritty --theme nord
```

### Available Themes
| Theme | Look | Best For |
|-------|------|----------|
| `tokyonight` | Blue & purple | Late-night coding |
| `catppuccin-mocha` | Purple & pink | Cozy setup |
| `catppuccin-latte` | Light pastel | Daytime use |
| `gruvbox-dark` | Warm browns | Retro feel |
| `rose-pine` | Soft pink/purple | Aesthetic |
| `nord` | Cool blue | Clean look |
| `solarized-dark` | Classic | Easy on eyes |

### List All Themes
```bash
bash linux/install.sh --list
```

### Preview Colors
```bash
bash linux/install.sh --preview
```

---

## Supported Terminals

| Terminal | Config Location |
|----------|-----------------|
| Kitty | `~/.config/kitty/kitty.conf` |
| Alacritty | `~/.config/alacritty/alacritty.toml` |
| WezTerm | `~/.config/wezterm/wezterm.lua` |

> **Note:** Windows Terminal is not available on Linux/macOS

---

## Troubleshooting

### "Permission denied"
```bash
chmod +x install.sh
```

### "Theme not applying"
1. Close and reopen your terminal
2. If using tmux: restart tmux (`tmux kill-server`)
3. Check your terminal supports true color (`curl -s https://raw.githubusercontent.com/JohnMorales/dotfiles/master/colors/24-bit.sh | bash`)

### "Terminal not found"
Make sure your terminal is installed:
- **Kitty**: `sudo apt install kitty` (Ubuntu/Debian) or `brew install kitty` (macOS)
- **Alacritty**: `sudo apt install alacritty` or `brew install alacritty`
- **WezTerm**: `brew install wezterm` (macOS) or see [wezfurlong.org](https://wezfurlong.org)

### "Git not available"
```bash
# Download as ZIP
curl -sL https://github.com/zenithopensourceprojects/projectkittythemes/archive/main.zip -o pkt.zip
unzip pkt.zip
cd pkt-main/linux
bash install.sh
```

---

## Need Help?

- Website: [View all themes](https://github.com/zenithopensourceprojects/projectkittythemes)
- Issues: [Open a ticket](https://github.com/zenithopensourceprojects/projectkittythemes/issues)
