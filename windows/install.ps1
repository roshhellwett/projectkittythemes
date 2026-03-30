<#
.SYNOPSIS
    ProjectKittyThemes Installer for Windows
.DESCRIPTION
    Installs terminal themes for Kitty, Alacritty, WezTerm, and Windows Terminal
#>

param(
    [string]$Terminal,
    [string]$Theme,
    [switch]$List,
    [switch]$Preview,
    [switch]$Help
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path $ScriptDir -Parent
$ThemesDir = Join-Path $ProjectRoot "themes"

function Show-Banner {
    Write-Host ""
    Write-Host "  =============================" -ForegroundColor Cyan
    Write-Host "  [=] ProjectKittyThemes [=]" -ForegroundColor Cyan -BackgroundColor DarkBlue
    Write-Host "  =============================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Usage {
    Write-Host "Usage: .\install.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Terminal <kitty|alacritty|wezterm|windows-terminal>  Select terminal"
    Write-Host "  -Theme <slug>                                         Select theme by slug"
    Write-Host "  -List                                                 List all themes"
    Write-Host "  -Preview                                              Preview colors in terminal"
    Write-Host "  -Help                                                 Show this help"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host '  .\install.ps1 -Terminal windows-terminal -Theme tokyonight'
    Write-Host "  .\install.ps1 -List"
    Write-Host "  .\install.ps1 -Preview"
}

function Get-Themes {
    $themes = @()
    Get-ChildItem -Path $ThemesDir -Directory | ForEach-Object {
        $themeJson = Join-Path $_.FullName "theme.json"
        if (Test-Path $themeJson) {
            $content = Get-Content $themeJson -Raw | ConvertFrom-Json
            $themes += [PSCustomObject]@{
                Name = $content.name
                Slug = $content.slug
                Category = $content.category -join ", "
            }
        }
    }
    return $themes
}

function Show-List {
    Write-Host "Available Themes:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host ([PSCustomObject]@{
        Theme = "Tokyo Night"
        Slug = "tokyonight"
        Category = "dark"
    } | Format-Table -AutoSize | Out-String)
    
    Write-Host ([PSCustomObject]@{
        Theme = "Catppuccin Mocha"
        Slug = "catppuccin-mocha"
        Category = "dark"
    } | Format-Table -AutoSize | Out-String)
    
    Write-Host ([PSCustomObject]@{
        Theme = "Catppuccin Latte"
        Slug = "catppuccin-latte"
        Category = "pastel"
    } | Format-Table -AutoSize | Out-String)
    
    Write-Host ([PSCustomObject]@{
        Theme = "Gruvbox Dark"
        Slug = "gruvbox-dark"
        Category = "dark"
    } | Format-Table -AutoSize | Out-String)
    
    Write-Host ([PSCustomObject]@{
        Theme = "Rose Pine"
        Slug = "rose-pine"
        Category = "pastel"
    } | Format-Table -AutoSize | Out-String)
    
    Write-Host ([PSCustomObject]@{
        Theme = "Nord"
        Slug = "nord"
        Category = "high-contrast"
    } | Format-Table -AutoSize | Out-String)
    
    Write-Host ([PSCustomObject]@{
        Theme = "Solarized Dark"
        Slug = "solarized-dark"
        Category = "high-contrast"
    } | Format-Table -AutoSize | Out-String)
}

function Show-Preview {
    $themes = Get-Themes
    foreach ($theme in $themes) {
        $themeJson = Join-Path $ThemesDir "$($theme.Slug)\theme.json"
        $content = Get-Content $themeJson -Raw | ConvertFrom-Json
        
        Write-Host "$($theme.Name)" -ForegroundColor Yellow
        Write-Host "  Background: $($content.background)"
        Write-Host "  Foreground: $($content.foreground)"
        
        $colors = @(
            $content.ansi_colors.black,
            $content.ansi_colors.red,
            $content.ansi_colors.green,
            $content.ansi_colors.yellow,
            $content.ansi_colors.blue,
            $content.ansi_colors.magenta,
            $content.ansi_colors.cyan,
            $content.ansi_colors.white
        )
        
        foreach ($color in $colors) {
            Write-Host -NoNewline "  "
            $rgb = $color -replace '#', ''
            $r = [Convert]::ToInt32($rgb.Substring(0, 2), 16)
            $g = [Convert]::ToInt32($rgb.Substring(2, 2), 16)
            $b = [Convert]::ToInt32($rgb.Substring(4, 2), 16)
            $ansi = 16 + [math]::Floor($r / 51) * 36 + [math]::Floor($g / 51) * 6 + [math]::Floor($b / 51)
            Write-Host -BackgroundColor $ansi -NoNewline "      "
        }
        Write-Host ""
        Write-Host ""
    }
}

function Get-WindowsTerminalSettingsPath {
    $wtPath = "$env:LOCALAPPDATA\Packages"
    if (Test-Path $wtPath) {
        $packages = Get-ChildItem -Path $wtPath -Directory | Where-Object { $_.Name -like "Microsoft.WindowsTerminal*" }
        if ($packages) {
            return Join-Path $packages[0].FullName "LocalState\settings.json"
        }
    }
    return $null
}

function Install-WindowsTerminalTheme {
    param(
        [string]$ThemeSlug,
        [string]$ThemeName
    )
    
    $settingsPath = Get-WindowsTerminalSettingsPath
    if (-not $settingsPath) {
        Write-Host "Windows Terminal not found. Please install it from Microsoft Store." -ForegroundColor Red
        return $false
    }
    
    $themeJson = Join-Path $ThemesDir "$ThemeSlug\windows-terminal.json"
    if (-not (Test-Path $themeJson)) {
        Write-Host "Theme config not found: $themeJson" -ForegroundColor Red
        return $false
    }
    
    try {
        $backupPath = "$settingsPath.backup"
        if (-not (Test-Path $backupPath)) {
            Copy-Item $settingsPath $backupPath
            Write-Host "Backed up settings to: $backupPath" -ForegroundColor Yellow
        }
        
        $settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
        
        $themeContent = Get-Content $themeJson -Raw | ConvertFrom-Json
        
        $existingScheme = $settings.schemes | Where-Object { $_.name -eq $ThemeName }
        if ($existingScheme) {
            $confirm = Read-Host "Theme already exists in schemes. Overwrite? [y/N]"
            if ($confirm -ne "y" -and $confirm -ne "Y") {
                Write-Host "Installation cancelled."
                return $false
            }
            $settings.schemes = @($settings.schemes | Where-Object { $_.name -ne $ThemeName })
        }
        
        $settings.schemes += $themeContent
        
        if ($settings.profiles -and $settings.profiles.defaults) {
            $settings.profiles.defaults | Add-Member -NotePropertyName "colorScheme" -NotePropertyValue $ThemeName -Force
        } elseif ($settings.profiles) {
            if (-not $settings.profiles.defaults) {
                $settings.profiles | Add-Member -NotePropertyName "defaults" -Value ([PSCustomObject]@{}) -Force
            }
            $settings.profiles.defaults | Add-Member -NotePropertyName "colorScheme" -NotePropertyValue $ThemeName -Force
        }
        
        $settings | ConvertTo-Json -Depth 10 | Set-Content $settingsPath -Encoding UTF8
        
        return $true
    }
    catch {
        Write-Host "Error installing theme: $_" -ForegroundColor Red
        if (Test-Path "$settingsPath.backup") {
            Copy-Item "$settingsPath.backup" $settingsPath -Force
            Write-Host "Restored from backup." -ForegroundColor Yellow
        }
        return $false
    }
}

function Install-KittyTheme {
    param(
        [string]$ThemeSlug
    )
    
    $configPath = "$env:APPDATA\kitty\kitty.conf"
    $themeConf = Join-Path $ThemesDir "$ThemeSlug\kitty.conf"
    
    if (-not (Test-Path $themeConf)) {
        Write-Host "Theme config not found: $themeConf" -ForegroundColor Red
        return $false
    }
    
    $configDir = Split-Path $configPath -Parent
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        Write-Host "Created config directory: $configDir" -ForegroundColor Yellow
    }
    
    if (Test-Path $configPath) {
        $confirm = Read-Host "Config exists. Overwrite? [y/N]"
        if ($confirm -ne "y" -and $confirm -ne "Y") {
            Write-Host "Installation cancelled."
            return $false
        }
        Copy-Item $configPath "$configPath.backup" -Force
        Write-Host "Backed up existing config to: $configPath.backup" -ForegroundColor Yellow
    }
    
    Copy-Item $themeConf $configPath -Force
    return $true
}

function Install-AlacrittyTheme {
    param(
        [string]$ThemeSlug
    )
    
    $configPath = "$env:APPDATA\alacritty\alacritty.toml"
    $themeToml = Join-Path $ThemesDir "$ThemeSlug\alacritty.toml"
    
    if (-not (Test-Path $themeToml)) {
        Write-Host "Theme config not found: $themeToml" -ForegroundColor Red
        return $false
    }
    
    $configDir = Split-Path $configPath -Parent
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        Write-Host "Created config directory: $configDir" -ForegroundColor Yellow
    }
    
    if (Test-Path $configPath) {
        $confirm = Read-Host "Config exists. Overwrite? [y/N]"
        if ($confirm -ne "y" -and $confirm -ne "Y") {
            Write-Host "Installation cancelled."
            return $false
        }
        Copy-Item $configPath "$configPath.backup" -Force
        Write-Host "Backed up existing config to: $configPath.backup" -ForegroundColor Yellow
    }
    
    Copy-Item $themeToml $configPath -Force
    return $true
}

function Install-WezTermTheme {
    param(
        [string]$ThemeSlug
    )
    
    $configPath = "$env:USERPROFILE\.wezterm.lua"
    $themeLua = Join-Path $ThemesDir "$ThemeSlug\wezterm.lua"
    
    if (-not (Test-Path $themeLua)) {
        Write-Host "Theme config not found: $themeLua" -ForegroundColor Red
        return $false
    }
    
    if (Test-Path $configPath) {
        $confirm = Read-Host "Config exists. Overwrite? [y/N]"
        if ($confirm -ne "y" -and $confirm -ne "Y") {
            Write-Host "Installation cancelled."
            return $false
        }
        Copy-Item $configPath "$configPath.backup" -Force
        Write-Host "Backed up existing config to: $configPath.backup" -ForegroundColor Yellow
    }
    
    Copy-Item $themeLua $configPath -Force
    return $true
}

function Install-Theme {
    param(
        [string]$Terminal,
        [string]$ThemeSlug
    )
    
    $themeJson = Join-Path $ThemesDir "$ThemeSlug\theme.json"
    if (-not (Test-Path $themeJson)) {
        Write-Host "Theme not found: $ThemeSlug" -ForegroundColor Red
        return $false
    }
    
    $content = Get-Content $themeJson -Raw | ConvertFrom-Json
    $themeName = $content.name
    
    switch ($Terminal.ToLower()) {
        "windows-terminal" {
            $result = Install-WindowsTerminalTheme -ThemeSlug $ThemeSlug -ThemeName $themeName
        }
        "kitty" {
            $result = Install-KittyTheme -ThemeSlug $ThemeSlug
        }
        "alacritty" {
            $result = Install-AlacrittyTheme -ThemeSlug $ThemeSlug
        }
        "wezterm" {
            $result = Install-WezTermTheme -ThemeSlug $ThemeSlug
        }
        default {
            Write-Host "Unknown terminal: $Terminal" -ForegroundColor Red
            return $false
        }
    }
    
    if ($result) {
        Write-Host ""
        Write-Host "Successfully installed $themeName!" -ForegroundColor Green
        Write-Host "Terminal: $Terminal" -ForegroundColor Cyan
        return $true
    }
    
    return $false
}

function Select-Terminal {
    Write-Host "Select terminal:" -ForegroundColor Yellow
    Write-Host "  1) Kitty"
    Write-Host "  2) Alacritty"
    Write-Host "  3) WezTerm"
    Write-Host "  4) Windows Terminal"
    Write-Host ""
    $choice = Read-Host "Enter choice [1-4]"
    
    switch ($choice) {
        "1" { return "kitty" }
        "2" { return "alacritty" }
        "3" { return "wezterm" }
        "4" { return "windows-terminal" }
        default { return "windows-terminal" }
    }
}

function Select-Theme {
    param([string]$Category)
    
    $themes = Get-Themes
    if ($Category -ne "all") {
        $themes = $themes | Where-Object { $_.Category -contains $Category }
    }
    
    Write-Host "Available themes:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $themes.Count; $i++) {
        Write-Host "  $($i + 1)) $($themes[$i].Name) ($($themes[$i].Slug))"
    }
    Write-Host ""
    $choice = Read-Host "Enter choice [1-$($themes.Count)]"
    
    if ([int]$choice -ge 1 -and [int]$choice -le $themes.Count) {
        return $themes[[int]$choice - 1].Slug
    }
    return $themes[0].Slug
}

function Select-Category {
    Write-Host "Select category:" -ForegroundColor Yellow
    Write-Host "  1) Dark"
    Write-Host "  2) Pastel"
    Write-Host "  3) High-Contrast"
    Write-Host "  4) All themes"
    Write-Host ""
    $choice = Read-Host "Enter choice [1-4]"
    
    switch ($choice) {
        "1" { return "dark" }
        "2" { return "pastel" }
        "3" { return "high-contrast" }
        "4" { return "all" }
        default { return "all" }
    }
}

try {
    if ($Help) {
        Show-Banner
        Show-Usage
        exit 0
    }
    
    if ($List) {
        Show-Banner
        Show-List
        exit 0
    }
    
    if ($Preview) {
        Show-Banner
        Show-Preview
        exit 0
    }
    
    Show-Banner
    
    $interactive = -not $Terminal -and -not $Theme
    
    if ($interactive) {
        $Terminal = Select-Terminal
        Write-Host ""
        $Category = Select-Category
        Write-Host ""
        $Theme = Select-Theme -Category $Category
        Write-Host ""
    }
    
    if (-not $Terminal) {
        Write-Host "Error: Terminal not specified" -ForegroundColor Red
        Show-Usage
        exit 1
    }
    
    if (-not $Theme) {
        Write-Host "Error: Theme not specified" -ForegroundColor Red
        Show-Usage
        exit 1
    }
    
    Install-Theme -Terminal $Terminal -ThemeSlug $Theme
    
    Write-Host ""
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "If execution policy is blocking, run:" -ForegroundColor Yellow
    Write-Host "  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned" -ForegroundColor Cyan
}
