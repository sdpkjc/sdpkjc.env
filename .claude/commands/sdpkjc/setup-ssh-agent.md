---
description: Configure 1Password CLI SSH Agent on this machine (macOS/Linux)
allowed-tools: Bash(*), Read, Write, Edit
---

# Setup 1Password SSH Agent

Help the user configure 1Password CLI SSH Agent on macOS or Linux.

## Steps to execute

### 1. Detect OS and check prerequisites

```bash
uname -s
```

**macOS:**
- Verify 1Password app: `ls /Applications/1Password.app`
- Check CLI: `which op`

**Linux:**
- Verify 1Password app: `which 1password` or check if installed via package manager
- Check CLI: `which op`
- **Important:** 1Password SSH agent does NOT work with Flatpak or Snap installations. Must use .deb/.rpm or other native install.

### 2. Create SSH directory and config

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
```

Check if `~/.ssh/config` exists and read its content.

### 3. Configure SSH to use 1Password agent

Add or update `~/.ssh/config` to include:

```
# 1Password SSH Agent
Host *
    IdentityAgent "~/.1password/agent.sock"
```

Make sure:
- Don't duplicate if already configured
- Preserve existing config content
- Set proper permissions: `chmod 600 ~/.ssh/config`

### 4. Remind user to enable SSH Agent in 1Password app

Tell the user:

> Please open 1Password app and go to:
> **Settings > Developer > Set Up SSH Agent**
>
> Recommended settings:
> - **macOS:** Settings > General > Enable "Keep 1Password in the menu bar" and "Start at login"
> - **Linux:** Settings > Security > Enable "Unlock using system authentication" for biometric support

### 5. Verify setup

```bash
# Check if agent socket exists
ls -la ~/.1password/agent.sock

# Test with GitHub (if user has GitHub SSH key in 1Password)
ssh -T git@github.com
```

## Platform-specific notes

### macOS
- Authentication via Touch ID / Apple Watch / password
- 1Password app must be running

### Linux
- Authentication via system authentication (fingerprint if configured) or password
- 1Password app must be running
- Flatpak/Snap versions do NOT support SSH agent - use native package install
- If using WSL, may need additional socket bridging configuration
