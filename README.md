#  _    _                     _             _____ _    _ _____ 
# | |  | |                   | |           / ____| |  | |_   _|
# | |  | |_ __   __ _ _ __ __| | ___ _ __ | |  __| |  | | | |  
# | |  | | '_ \ / _` | '__/ _` |/ _ \ '_ \| | |_ | |  | | | |  
# | |__| | |_) | (_| | | | (_| |  __/ | | | |__| | |__| |_| |_ 
#  \____/| .__/ \__,_|_|  \__,_|\___|_| |_|\_____|\____/|_____|
#        | |                                                      
#        |_|                                                      
#
# ProjectKittyThemes

[![Themes](https://img.shields.io/badge/7-Themes-ff6b6b?style=flat-square)](themes)
[![Terminals](https://img.shields.io/badge/4-Termemes-4ecdc4?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-45b7d1?style=flat-square)](LICENSE)

Beautiful color themes for your terminal. Transform your terminal from boring default colors to something you'll love.

---

## 🎨 Preview Themes

[Open Web Gallery →](web/index.html)

Or see all themes below:

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

## ⚡ Quick Install (Copy & Paste)

### Windows

**Option 1 - Recommended** (PowerShell):
```powershell
irm https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/windows/install.ps1 | iex
```

**Option 2** - Download the app:
- Go to [`windows/`](windows/) folder
- Download `ProjectKittyThemes-Manager.exe`
- Double-click to run

### Linux / macOS

```bash
bash <(curl -s https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main/linux/install.sh)
```

---

## 🤔 Need Help?

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

### "Command not found" or "Permission denied"

**Windows:**
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Linux/macOS:**
```bash
chmod +x install.sh
```

### "My terminal still looks the same"

1. **Restart your terminal completely** (close all windows)
2. For Windows Terminal: open a NEW tab
3. Make sure only ONE theme is installed at a time

### Need more help?

- [Windows Installation Guide](windows/README.md)
- [Linux/macOS Installation Guide](linux/README.md)
- [Open an Issue](https://github.com/zenithopensourceprojects/projectkittythemes/issues)

---

## Contributing

Want to add a new theme? See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT License - Free to use, modify, and share.
