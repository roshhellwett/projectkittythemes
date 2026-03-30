#!/usr/bin/env bash
# ===========================
# Palette SVG Generator
# ProjectKittyThemes
# ===========================

set -e

THEMES_DIR="$(cd "$(dirname "$0")/.." && pwd)/themes"

generate_svg() {
    local theme_json="$1"
    local output_path="$2"
    local theme_name=$(python3 -c "import json; print(json.load(open('$theme_json'))['name'])")
    local slug=$(python3 -c "import json; print(json.load(open('$theme_json'))['slug'])")
    
    local colors=$(python3 -c "
import json
with open('$theme_json') as f:
    data = json.load(f)
    ansi = data['ansi_colors']
    colors = [
        ansi['black'], ansi['red'], ansi['green'], ansi['yellow'],
        ansi['blue'], ansi['magenta'], ansi['cyan'], ansi['white'],
        ansi['bright_black'], ansi['bright_red'], ansi['bright_green'], ansi['bright_yellow'],
        ansi['bright_blue'], ansi['bright_magenta'], ansi['bright_cyan'], ansi['bright_white']
    ]
    names = ['Black', 'Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan', 'White',
             'Bright Black', 'Bright Red', 'Bright Green', 'Bright Yellow',
             'Bright Blue', 'Bright Magenta', 'Bright Cyan', 'Bright White']
    for i, (c, n) in enumerate(zip(colors, names)):
        print(f'{c}|{n}')
" 2>/dev/null)

    cat > "$output_path" << 'SVGEOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="200" fill="#1a1a1a"/>
SVGEOF

    local y=10
    local row=0
    local idx=0
    
    while IFS='|' read -r color name; do
        local x=$((idx * 100))
        
        local luminance=$(python3 -c "
import sys
c = '$color'.lstrip('#')
r = int(c[0:2], 16) / 255
g = int(c[2:4], 16) / 255
b = int(c[4:6], 16) / 255
l = 0.2126 * r + 0.7152 * g + 0.0722 * b
print('white' if l > 0.5 else 'black')
")
        
        if [ $idx -eq 8 ]; then
            y=110
            x=0
        fi
        
        local adjusted_x=$((idx * 100))
        if [ $idx -ge 8 ]; then
            adjusted_x=$(((idx - 8) * 100))
        fi

        cat >> "$output_path" << SVGEOF
  <rect x="$adjusted_x" y="$y" width="100" height="100" fill="$color"/>
  <text x="$((adjusted_x + 50))" y="$((y + 60))" font-family="monospace" font-size="11" fill="$luminance" text-anchor="middle">$name</text>
  <text x="$((adjusted_x + 50))" y="$((y + 75))" font-family="monospace" font-size="9" fill="$luminance" text-anchor="middle">$color</text>
SVGEOF

        idx=$((idx + 1))
    done <<< "$colors"
    
    cat >> "$output_path" << SVGEOF
</svg>
SVGEOF
    
    echo "Generated: $output_path"
}

echo "Generating palette SVGs..."
echo ""

for theme_dir in "$THEMES_DIR"/*; do
    if [ -d "$theme_dir" ]; then
        theme_json="$theme_dir/theme.json"
        if [ -f "$theme_json" ]; then
            output_path="$theme_dir/palette.svg"
            generate_svg "$theme_json" "$output_path"
        fi
    fi
done

echo ""
echo "Done! Generated $(ls -1 "$THEMES_DIR"/*/palette.svg 2>/dev/null | wc -l) palette SVGs"
