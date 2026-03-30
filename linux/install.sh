#!/usr/bin/env bash
# ===========================
# ProjectKittyThemes Installer
# Linux/Mac
# ===========================

set -e

RESET='\033[0m'
BOLD='\033[1m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
THEMES_DIR="$(cd "$SCRIPT_DIR/.." && pwd)/themes"
REPO_URL="https://raw.githubusercontent.com/zenithopensourceprojects/projectkittythemes/main"

show_banner() {
    echo -e "${BOLD}${CYAN}"
    echo "  🐱 ProjectKittyThemes Installer"
    echo -e "${RESET}"
    echo "  ============================"
    echo ""
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --terminal <kitty|alacritty|wezterm|windows-terminal>  Select terminal"
    echo "  --theme <slug>                                         Select theme by slug"
    echo "  --list                                                 List all themes"
    echo "  --preview                                              Preview colors in terminal"
    echo "  --help                                                 Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 --terminal kitty --theme tokyonight"
    echo "  $0 --list"
    echo "  $0 --preview"
}

list_themes() {
    echo -e "${BOLD}Available Themes:${RESET}"
    echo ""
    printf "%-20s %-20s %s\n" "Theme" "Slug" "Category"
    printf "%-20s %-20s %s\n" "------" "----" "--------"
    
    for theme_dir in "$THEMES_DIR"/*; do
        if [ -d "$theme_dir" ] && [ -f "$theme_dir/theme.json" ]; then
            name=$(grep '"name"' "$theme_dir/theme.json" | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
            slug=$(basename "$theme_dir")
            category=$(grep '"category"' "$theme_dir/theme.json" | head -1 | sed 's/.*: *\[\([^]]*\)\].*/\1/' | tr -d '"')
            printf "%-20s %-20s %s\n" "$name" "$slug" "$category"
        fi
    done
    echo ""
}

preview_colors() {
    for theme_dir in "$THEMES_DIR"/*; do
        if [ -d "$theme_dir" ] && [ -f "$theme_dir/theme.json" ]; then
            name=$(grep '"name"' "$theme_dir/theme.json" | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
            echo -e "${BOLD}$name${RESET}"
            echo -e "Background: $(grep '"background"' "$theme_dir/theme.json" | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')"
            echo -e "Foreground: $(grep '"foreground"' "$theme_dir/theme.json" | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')"
            
            colors=$(grep -A 16 '"ansi_colors"' "$theme_dir/theme.json" | grep -E '^\s*"(black|red|green|yellow|blue|magenta|cyan|white|bright_)":' | sed 's/.*: *"\([^"]*\)".*/\1/')
            
            for color in $colors; do
                printf "\033[48;5;%dm     \033[0m" $(python3 -c "c='$color'.lstrip('#');print(int(c[:2],16)//11*36+int(c[2:4],16)//11*6+int(c[4:6],16)//11+16)" 2>/dev/null || echo "232")
            done
            echo " $color"
            echo ""
        fi
    done
}

get_themes_by_category() {
    local category="$1"
    local themes=()
    
    for theme_dir in "$THEMES_DIR"/*; do
        if [ -d "$theme_dir" ] && [ -f "$theme_dir/theme.json" ]; then
            if grep -q "\"$category\"" "$theme_dir/theme.json"; then
                themes+=("$(basename "$theme_dir")")
            fi
        fi
    done
    
    printf '%s\n' "${themes[@]}"
}

select_terminal() {
    echo -e "${BOLD}Select terminal:${RESET}"
    echo "  1) Kitty"
    echo "  2) Alacritty"
    echo "  3) WezTerm"
    echo "  4) Windows Terminal"
    echo ""
    read -p "Enter choice [1-4]: " choice
    
    case $choice in
        1) echo "kitty" ;;
        2) echo "alacritty" ;;
        3) echo "wezterm" ;;
        4) echo "windows-terminal" ;;
        *) echo "kitty" ;;
    esac
}

select_category() {
    echo -e "${BOLD}Select category:${RESET}"
    echo "  1) Dark"
    echo "  2) Pastel"
    echo "  3) High-Contrast"
    echo "  4) All themes"
    echo ""
    read -p "Enter choice [1-4]: " choice
    
    case $choice in
        1) echo "dark" ;;
        2) echo "pastel" ;;
        3) echo "high-contrast" ;;
        4) echo "all" ;;
        *) echo "all" ;;
    esac
}

select_theme() {
    local category="$1"
    local themes=()
    local names=()
    
    if [ "$category" = "all" ]; then
        for theme_dir in "$THEMES_DIR"/*; do
            if [ -d "$theme_dir" ] && [ -f "$theme_dir/theme.json" ]; then
                slug=$(basename "$theme_dir")
                name=$(grep '"name"' "$theme_dir/theme.json" | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
                themes+=("$slug")
                names+=("$name")
            fi
        done
    else
        for theme_dir in "$THEMES_DIR"/*; do
            if [ -d "$theme_dir" ] && [ -f "$theme_dir/theme.json" ]; then
                if grep -q "\"$category\"" "$theme_dir/theme.json"; then
                    slug=$(basename "$theme_dir")
                    name=$(grep '"name"' "$theme_dir/theme.json" | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
                    themes+=("$slug")
                    names+=("$name")
                fi
            fi
        done
    fi
    
    echo -e "${BOLD}Available themes:${RESET}"
    for i in "${!themes[@]}"; do
        echo "  $((i+1))) ${names[$i]} (${themes[$i]})"
    done
    echo ""
    read -p "Enter choice [1-${#themes[@]}]: " choice
    
    if [ "$choice" -ge 1 ] && [ "$choice" -le "${#themes[@]}" ]; then
        echo "${themes[$((choice-1))]}"
    else
        echo "${themes[0]}"
    fi
}

get_config_path() {
    local terminal="$1"
    
    case $terminal in
        kitty)
            echo "$HOME/.config/kitty/kitty.conf"
            ;;
        alacritty)
            echo "$HOME/.config/alacritty/alacritty.toml"
            ;;
        wezterm)
            echo "$HOME/.config/wezterm/theme.lua"
            ;;
        windows-terminal)
            echo "$HOME/.config/windows-terminal/settings.json"
            ;;
    esac
}

get_source_file() {
    local terminal="$1"
    local theme_dir="$2"
    
    case $terminal in
        kitty)
            echo "$theme_dir/kitty.conf"
            ;;
        alacritty)
            echo "$theme_dir/alacritty.toml"
            ;;
        wezterm)
            echo "$theme_dir/wezterm.lua"
            ;;
        windows-terminal)
            echo "$theme_dir/windows-terminal.json"
            ;;
    esac
}

install_theme() {
    local terminal="$1"
    local theme_slug="$2"
    
    local theme_dir="$THEMES_DIR/$theme_slug"
    local theme_json="$theme_dir/theme.json"
    
    if [ ! -d "$theme_dir" ]; then
        echo -e "${RED}Error: Theme '$theme_slug' not found${RESET}"
        exit 1
    fi
    
    if [ ! -f "$theme_json" ]; then
        echo -e "${RED}Error: theme.json not found for '$theme_slug'${RESET}"
        exit 1
    fi
    
    local theme_name=$(grep '"name"' "$theme_json" | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
    local config_path
    config_path=$(get_config_path "$terminal")
    
    local config_dir=$(dirname "$config_path")
    
    if [ ! -d "$config_dir" ]; then
        echo -e "${YELLOW}Creating config directory: $config_dir${RESET}"
        mkdir -p "$config_dir"
    fi
    
    local source_file
    source_file=$(get_source_file "$terminal" "$theme_dir")
    
    if [ ! -f "$source_file" ]; then
        echo -e "${RED}Error: Config file not found: $source_file${RESET}"
        exit 1
    fi
    
    if [ -f "$config_path" ]; then
        echo -e "${YELLOW}Config file exists: $config_path${RESET}"
        read -p "Theme already applied. Overwrite? [y/N]: " confirm
        
        if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
            echo "Installation cancelled."
            exit 0
        fi
        
        if [ "$terminal" = "kitty" ]; then
            if grep -q "include.*current-theme.conf" "$config_path" 2>/dev/null; then
                cp "$config_path" "$config_path.backup"
                echo -e "${GREEN}Backed up existing config to: $config_path.backup${RESET}"
            fi
        else
            cp "$config_path" "$config_path.backup"
            echo -e "${GREEN}Backed up existing config to: $config_path.backup${RESET}"
        fi
    fi
    
    case $terminal in
        kitty)
            cp "$source_file" "$config_path"
            if ! grep -q "include.*current-theme.conf" "$config_path" 2>/dev/null; then
                echo "" >> "$config_path"
                echo "include current-theme.conf" >> "$config_path"
            fi
            ;;
        alacritty)
            cp "$source_file" "$config_path"
            ;;
        wezterm)
            cp "$source_file" "$config_path"
            ;;
        windows-terminal)
            echo -e "${RED}Windows Terminal requires manual configuration on Linux/Mac${RESET}"
            exit 1
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}✅ Successfully installed ${BOLD}$theme_name${RESET}${GREEN}!${RESET}"
    echo ""
    echo "Terminal: $terminal"
    echo "Config: $config_path"
    echo ""
}

main() {
    local terminal=""
    local theme=""
    local interactive=false
    
    if [ $# -eq 0 ]; then
        interactive=true
    fi
    
    while [ $# -gt 0 ]; do
        case "$1" in
            --terminal)
                terminal="$2"
                shift 2
                ;;
            --theme)
                theme="$2"
                shift 2
                ;;
            --list)
                show_banner
                list_themes
                exit 0
                ;;
            --preview)
                show_banner
                preview_colors
                exit 0
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                echo -e "${RED}Unknown option: $1${RESET}"
                show_usage
                exit 1
                ;;
        esac
    done
    
    show_banner
    
    if [ "$interactive" = true ]; then
        terminal=$(select_terminal)
        echo ""
        category=$(select_category)
        echo ""
        theme=$(select_theme "$category")
        echo ""
    fi
    
    if [ -z "$terminal" ]; then
        echo -e "${RED}Error: Terminal not specified${RESET}"
        show_usage
        exit 1
    fi
    
    if [ -z "$theme" ]; then
        echo -e "${RED}Error: Theme not specified${RESET}"
        show_usage
        exit 1
    fi
    
    install_theme "$terminal" "$theme"
}

main "$@"
