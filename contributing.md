# Contributing to Project Kitty Themes

Thank you for your interest in contributing! This project aims to provide beautiful terminal themes for everyone.

## Ways to Contribute

- **Submit new themes** - Add a new color scheme
- **Report bugs** - Help us improve stability
- **Suggest features** - Share your ideas
- **Improve documentation** - Help others get started
- **Share the project** - Star us on GitHub!

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Development Setup

```bash
# Clone the repository
git clone https://github.com/zenithopensourceprojects/projectkittythemes.git
cd projectkittythemes

# Install in development mode
pip install -e .

# Run tests
pip install -e ".[dev]"
pytest
```

### Project Structure

```
projectkittythemes/
├── src/projectkittythemes/
│   ├── cli.py           # Main CLI commands
│   ├── themes.py        # Theme loading utilities
│   ├── installer.py     # Installation logic
│   └── themes/          # Theme configurations
│       ├── theme-name/
│       │   ├── theme.json
│       │   ├── kitty.conf
│       │   ├── alacritty.toml
│       │   ├── wezterm.lua
│       │   ├── windows-terminal.json
│       │   └── palette.svg
```

## Adding a New Theme

1. Create a new folder in `src/projectkittythemes/themes/`
2. Add `theme.json` with theme metadata:
   ```json
   {
     "name": "Your Theme Name",
     "slug": "your-theme",
     "author": "Your Name",
     "category": ["dark"],
     "background": "#hex",
     "foreground": "#hex",
     "ansi_colors": {
       "black": "#hex",
       "red": "#hex",
       ...
     }
   }
   ```
3. Add terminal config files:
   - `kitty.conf` for Kitty
   - `alacritty.toml` for Alacritty
   - `wezterm.lua` for WezTerm
   - `windows-terminal.json` for Windows Terminal

## Coding Standards

- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small
- Test your changes before submitting

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Communication

- **Issues**: Open a GitHub issue for bugs or features
- **Discussions**: Use GitHub Discussions for questions

---

© 2026 [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/). All Rights Reserved. Zenith is a Open Source Project Idea's by @roshhellwett