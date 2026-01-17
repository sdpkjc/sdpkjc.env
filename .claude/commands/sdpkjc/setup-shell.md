---
description: Deploy shell configs from sdpkjc.env to home directory
allowed-tools: Bash(*), Read, Edit
---

# Setup Shell Configuration

Help the user deploy shell configuration files from this repo to their home directory.

## Steps to execute

### 1. Locate the sdpkjc.env repo

Find the repo path. It should be at the path where this command is being run from, or search for it:

```bash
# Check if we're in the repo
ls -la shell/.zshrc 2>/dev/null || echo "Not in sdpkjc.env repo"
```

### 2. Show current shell config status

Check what configs already exist in home:

```bash
for f in .zshrc .bashrc .aliases .exports .env_presets; do
    if [ -L "$HOME/$f" ]; then
        echo "SYMLINK: $f -> $(readlink "$HOME/$f")"
    elif [ -f "$HOME/$f" ]; then
        echo "FILE: $f (will be backed up)"
    else
        echo "MISSING: $f"
    fi
done
```

### 3. Run the setup script

Execute the shell setup:

```bash
./setup.sh shell
```

This will:
- Backup existing files (if not symlinks) with timestamp
- Create symlinks from `~` to the repo's `shell/` directory
- Link: `.zshrc`, `.bashrc`, `.aliases`, `.exports`, `.env_presets`

### 4. Verify the setup

```bash
ls -la ~/.zshrc ~/.bashrc ~/.aliases ~/.exports ~/.env_presets 2>/dev/null | grep -E "^l"
```

### 5. Remind user to reload shell

Tell the user:

> Shell configs deployed! To apply changes:
> ```bash
> source ~/.zshrc   # for zsh
> source ~/.bashrc  # for bash
> ```
> Or restart your terminal.

## Notes

- Existing non-symlink files are backed up with `.backup.YYYYMMDDHHMMSS` suffix
- Symlinks point to the repo, so editing either location updates the config
- Make sure to commit changes to the repo to persist across machines
