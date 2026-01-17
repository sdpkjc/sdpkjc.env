# ============================================================
# sdpkjc's bashrc
# ============================================================

# If not interactive, don't do anything
[[ $- != *i* ]] && return

# Load exports
[ -f ~/.exports ] && source ~/.exports

# Load aliases
[ -f ~/.aliases ] && source ~/.aliases

# Load environment presets
[ -f ~/.env_presets ] && source ~/.env_presets

# ============================================================
# Bash Options
# ============================================================

shopt -s autocd         # cd by typing directory name
shopt -s cdspell        # autocorrect cd typos
shopt -s histappend     # append to history file
shopt -s checkwinsize   # update window size after commands

# ============================================================
# Prompt (Starship)
# ============================================================

if command -v starship &> /dev/null; then
    eval "$(starship init bash)"
fi

# ============================================================
# Tools Init
# ============================================================

# fzf
[ -f ~/.fzf.bash ] && source ~/.fzf.bash

# zoxide
if command -v zoxide &> /dev/null; then
    eval "$(zoxide init bash)"
fi

# ============================================================
# Local config (not tracked)
# ============================================================

[ -f ~/.bashrc.local ] && source ~/.bashrc.local
