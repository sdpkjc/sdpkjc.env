# ============================================================
# sdpkjc's zshrc
# ============================================================

# Load exports
[ -f ~/.exports ] && source ~/.exports

# Load aliases
[ -f ~/.aliases ] && source ~/.aliases

# ============================================================
# Zsh Options
# ============================================================

setopt AUTO_CD              # cd by typing directory name
setopt CORRECT              # command correction
setopt HIST_IGNORE_DUPS     # ignore duplicates in history
setopt SHARE_HISTORY        # share history across sessions
setopt APPEND_HISTORY       # append to history file

# ============================================================
# Completion
# ============================================================

autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'

# ============================================================
# Prompt (Starship)
# ============================================================

if command -v starship &> /dev/null; then
    eval "$(starship init zsh)"
fi

# ============================================================
# Tools Init
# ============================================================

# fzf
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# zoxide
if command -v zoxide &> /dev/null; then
    eval "$(zoxide init zsh)"
fi

# ============================================================
# Local config (not tracked)
# ============================================================

[ -f ~/.zshrc.local ] && source ~/.zshrc.local
