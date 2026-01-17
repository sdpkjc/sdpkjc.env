#!/bin/bash

# ============================================================
# sdpkjc.env setup script
# Creates symlinks from ~ to config files in this repo
# ============================================================

set -e

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ============================================================
# Symlink function
# ============================================================

link_file() {
    local src="$1"
    local dest="$2"

    if [ ! -e "$src" ]; then
        error "Source not found: $src"
        return 1
    fi

    # Backup existing file if it's not a symlink
    if [ -e "$dest" ] && [ ! -L "$dest" ]; then
        local backup="${dest}.backup.$(date +%Y%m%d%H%M%S)"
        warn "Backing up existing $dest to $backup"
        mv "$dest" "$backup"
    fi

    # Remove existing symlink
    if [ -L "$dest" ]; then
        rm "$dest"
    fi

    # Create parent directory if needed
    mkdir -p "$(dirname "$dest")"

    # Create symlink
    ln -s "$src" "$dest"
    success "Linked $dest -> $src"
}

# ============================================================
# Setup functions by category
# ============================================================

setup_shell() {
    info "Setting up shell configs..."
    link_file "$DOTFILES_DIR/shell/.zshrc" "$HOME/.zshrc"
    link_file "$DOTFILES_DIR/shell/.bashrc" "$HOME/.bashrc"
    link_file "$DOTFILES_DIR/shell/.aliases" "$HOME/.aliases"
    link_file "$DOTFILES_DIR/shell/.exports" "$HOME/.exports"
    link_file "$DOTFILES_DIR/shell/.env_presets" "$HOME/.env_presets"
}

setup_git() {
    info "Setting up git configs..."
    link_file "$DOTFILES_DIR/git/.gitconfig" "$HOME/.gitconfig"
    link_file "$DOTFILES_DIR/git/.gitignore_global" "$HOME/.gitignore_global"
}

setup_terminal() {
    info "Setting up terminal configs..."
    link_file "$DOTFILES_DIR/terminal/starship.toml" "$HOME/.config/starship.toml"
    link_file "$DOTFILES_DIR/terminal/.tmux.conf" "$HOME/.tmux.conf"
}

setup_editors() {
    info "Setting up editor configs..."
    link_file "$DOTFILES_DIR/editors/vim/.vimrc" "$HOME/.vimrc"
    link_file "$DOTFILES_DIR/editors/nvim" "$HOME/.config/nvim"
    link_file "$DOTFILES_DIR/editors/vscode/settings.json" "$HOME/Library/Application Support/Code/User/settings.json"
}

# ============================================================
# Main
# ============================================================

show_help() {
    echo "Usage: ./setup.sh [options]"
    echo ""
    echo "Options:"
    echo "  all       Setup everything"
    echo "  shell     Setup shell configs (.zshrc, .bashrc, etc)"
    echo "  git       Setup git configs"
    echo "  terminal  Setup terminal configs (starship, tmux)"
    echo "  editors   Setup editor configs (vim, nvim, vscode)"
    echo "  help      Show this help"
    echo ""
    echo "Example:"
    echo "  ./setup.sh shell      # Only setup shell"
    echo "  ./setup.sh all        # Setup everything"
}

main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║       sdpkjc.env Setup                 ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo "DOTFILES_DIR: $DOTFILES_DIR"
    echo ""

    case "${1:-help}" in
        all)
            setup_shell
            [ -d "$DOTFILES_DIR/git" ] && setup_git
            [ -d "$DOTFILES_DIR/terminal" ] && setup_terminal
            [ -d "$DOTFILES_DIR/editors" ] && setup_editors
            ;;
        shell)
            setup_shell
            ;;
        git)
            setup_git
            ;;
        terminal)
            setup_terminal
            ;;
        editors)
            setup_editors
            ;;
        help|*)
            show_help
            exit 0
            ;;
    esac

    echo ""
    success "Setup complete! Restart your shell or run: source ~/.zshrc"
}

main "$@"
