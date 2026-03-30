# Contributing to ProjectKittyThemes

Thank you for your interest in contributing! This guide will help you add new themes to the collection.

## How to Add a New Theme

### Step 1: Create the Theme Directory

Create a new folder in `themes/` with your theme's slug (lowercase, hyphenated):

```bash
mkdir themes/my-awesome-theme
```

### Step 2: Create Required Files

Each theme must include these files:

- [ ] `theme.json` - Metadata and color definitions
- [ ] `kitty.conf` - Kitty Terminal config
- [ ] `alacritty.toml` - Alacritty config
- [ ] `wezterm.lua` - WezTerm config
- [ ] `windows-terminal.json` - Windows Terminal config
- [ ] `palette.svg` - Visual palette preview (generated via `linux/preview.sh`)

### Step 3: Create theme.json

Use this exact schema:

```json
{
  "name": "Theme Name",
  "slug": "theme-slug",
  "author": "author-name",
  "license": "MIT",
  "category": ["dark"],
  "tags": ["dark", "blue"],
  "background": "#000000",
  "foreground": "#ffffff",
  "accent": "#000000",
  "cursor": "#ffffff",
  "selection": "#000000",
  "ansi_colors": {
    "black": "#000000",
    "red": "#000000",
    "green": "#000000",
    "yellow": "#000000",
    "blue": "#000000",
    "magenta": "#000000",
    "cyan": "#000000",
    "white": "#000000",
    "bright_black": "#000000",
    "bright_red": "#000000",
    "bright_green": "#000000",
    "bright_yellow": "#000000",
    "bright_blue": "#000000",
    "bright_magenta": "#000000",
    "bright_cyan": "#000000",
    "bright_white": "#000000"
  },
  "terminals": ["kitty", "alacritty", "wezterm", "windows-terminal"],
  "preview_image": "preview.png",
  "palette_image": "palette.png"
}
```

### Step 4: Create Terminal Configs

Use the exact format specified in the repository. See existing themes for reference:

- `kitty.conf` format: Standard Kitty color directives
- `alacritty.toml` format: TOML with `[colors.primary]`, `[colors.normal]`, etc.
- `wezterm.lua` format: Lua table with `colors.ansi` and `colors.brights` arrays
- `windows-terminal.json` format: Windows Terminal scheme JSON

### Step 5: Generate Palette SVG

Run the preview script to generate the palette image:

```bash
bash linux/preview.sh
```

### Step 6: Update Category Files

Add your theme to the appropriate category file in `categories/`:

- `dark.md` - For dark themes
- `pastel.md` - For pastel/light themes
- `high-contrast.md` - For high contrast themes

## Color Accuracy Requirements

1. **Background/Foreground Contrast**: Ensure sufficient contrast for readability (WCAG AA minimum)
2. **ANSI Colors**: Include all 16 colors (8 normal + 8 bright)
3. **Accurate Hex Values**: Use the exact hex values from the original theme
4. **Cursor Color**: Should be visible against both background and text
5. **Selection Colors**: selection_background should be semi-transparent

## Testing Before Submitting

### Local Testing

1. **Kitty**: Restart Kitty and verify colors apply
2. **Alacritty**: Reload config and check colors
3. **WezTerm**: Run `:reload-config` and verify
4. **Windows Terminal**: Open a new tab to see changes

### Visual Checklist

- [ ] All 16 colors are distinct and visible
- [ ] Text is readable against all background colors
- [ ] Cursor is visible in both light and dark areas
- [ ] Selection highlight is visible but not overwhelming

## Pull Request Checklist

Before submitting a PR:

- [ ] All required files created
- [ ] theme.json is valid JSON
- [ ] All config files parse correctly
- [ ] Colors match the original theme exactly
- [ ] Category assigned correctly
- [ ] Documentation updated

## Theme.json Schema Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Display name of the theme |
| slug | string | Yes | URL-safe identifier |
| author | string | Yes | Original theme author |
| license | string | Yes | License (MIT, GPL, etc.) |
| category | array | Yes | dark, pastel, or high-contrast |
| tags | array | Yes | Descriptive tags |
| background | hex | Yes | Main background color |
| foreground | hex | Yes | Main text color |
| accent | hex | Yes | Primary accent color |
| cursor | hex | Yes | Cursor color |
| selection | hex | Yes | Selection background |
| ansi_colors | object | Yes | All 16 ANSI colors |
| terminals | array | Yes | Supported terminals |

## Questions?

Open an issue if you have questions or need help!
