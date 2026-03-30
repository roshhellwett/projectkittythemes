# PROJECT KITTY THEMES

[![Themes](https://img.shields.io/badge/7-Themes-ff6b6b?style=flat-square)](themes)
[![Terminals](https://img.shields.io/badge/4-Termemes-4ecdc4?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-45b7d1?style=flat-square)](LICENSE)

Beautiful color themes for your terminal. Transform your terminal from boring default colors to something you'll love.

---

## Preview Themes

### Web Gallery (Best for browsing)

1. Open `web/index.html` in your browser (double-click the file)
2. Click on any theme card to see all 16 colors
3. Click "Copy Install Command" to copy the install command

### Full Installation

See all themes below:

| Theme | Look | Best For |
|-------|------|----------|
| **Tokyo Night** | Blue & purple, modern | Late-night coding |
| **Catppuccin Mocha** | Purple & pink, cozy | Catppuccin fans |
| **Catppuccin Latte** | Light pastel | Daytime use |
| **Gruvbox Dark** | Warm browns, retro | Retro lovers |
| **Rosé Pine** | Soft pink & purple | Aesthetic setups |
| **Nord** | Cool blue, clean | Maximum readability |
| **Solarized Dark** | Classic, easy on eyes | Long reading sessions |

---

## Quick Install (Copy & Paste)

### Windows

**Option 1 - Recommended** (PowerShell):
```powershell
irm https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/windows/install.ps1 | iex
```

**Option 2** - Download the app:
- Go to [`windows/`](windows/) folder
- Download `ProjectKittyThemes.exe`
- Double-click to run

### Linux / macOS

```bash
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/linux/install.sh)
```

---

## Need Help?

### "I don't know what terminal I use"

No problem! Run this command:

**Windows (PowerShell):**
```powershell
$env:TERM_PROGRAM
```

**Linux/macOS:**
```bash
echo $TERM_PROGRAM
```

Still unsure? Just run the installer - it will auto-detect your terminal!

### "What if I pick the wrong theme?"

No worries! The installer creates a backup before making changes. You can:
- Run the installer again to pick a different theme
- Delete the backup file to restore your original colors

### "Theme not showing?"

1. Close and reopen your terminal completely
2. If using Windows Terminal: open a new tab
3. Still not working? Check our [Troubleshooting Guide](#troubleshooting)

---

## 📖 How It Works

1. **Download** - Copy the install command above
2. **Run** - Paste in your terminal and press Enter
3. **Select** - Choose your terminal and theme (or let it auto-detect)
4. **Restart** - Close and reopen your terminal to see the new colors!

That's it! 🎉

---

## Supported Terminals

| Terminal | Windows | Linux | macOS |
|----------|---------|-------|-------|
| Windows Terminal | ✅ | - | - |
| Kitty | ✅ | ✅ | ✅ |
| Alacritty | ✅ | ✅ | ✅ |
| WezTerm | ✅ | ✅ | ✅ |

---

## Troubleshooting

##### ----> "Command not found" or "Permission denied" <----

**Windows:**
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Linux/macOS:**
```bash
chmod +x install.sh
```

---

© 2026 [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/). All Rights Reserved. Zenith is a Open Source Project Idea's by @roshhellwett
