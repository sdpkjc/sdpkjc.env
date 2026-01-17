#!/usr/bin/env python3
"""sdpkjc.env installer - Interactive software installer for macOS/Linux"""

import subprocess
import sys
import platform
import shutil
from dataclasses import dataclass
from typing import Callable, Optional

# Auto-install rich if not available
try:
    from rich.console import Console
    from rich.table import Table
    from rich.prompt import Prompt
    from rich.panel import Panel
    from rich import box
except ImportError:
    print("Installing rich...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.table import Table
    from rich.prompt import Prompt
    from rich.panel import Panel
    from rich import box

console = Console()
OS = "macos" if platform.system() == "Darwin" else "linux"


# ============================================================
# Utilities
# ============================================================

def command_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run(cmd: str) -> int:
    return subprocess.call(cmd, shell=True)


def brew_install(pkg: str):
    run(f"brew install {pkg}")


def apt_install(pkg: str):
    run(f"sudo apt-get update && sudo apt-get install -y {pkg}")


def npm_install(pkg: str):
    run(f"npm install -g {pkg}")


def curl_install(url: str):
    run(f"curl -fsSL {url} | bash")


def curl_sh_install(url: str, args: str = ""):
    run(f"curl -fsSL {url} | sh -s -- {args}")


# ============================================================
# Software Definition
# ============================================================

@dataclass
class Software:
    name: str
    check_cmd: Optional[str]  # None = always show as runnable (npx tools)
    install: Callable
    category: str  # "base" or "vibe"

    def is_installed(self) -> bool:
        if self.check_cmd is None:
            return False  # npx tools, always "runnable"
        return command_exists(self.check_cmd)

    def run_install(self):
        if self.check_cmd and self.is_installed():
            console.print(f"[green]{self.name} already installed[/green]")
            return
        console.print(f"[blue]Installing {self.name}...[/blue]")
        self.install()


# ============================================================
# Install Functions
# ============================================================

def install_homebrew():
    run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
    if OS == "linux":
        run('echo \'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"\' >> ~/.bashrc')


def install_git():
    brew_install("git") if OS == "macos" else apt_install("git")


def install_tmux():
    brew_install("tmux") if OS == "macos" else apt_install("tmux")


def install_nodejs():
    curl_install("https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh")
    console.print("[yellow]Run 'nvm install --lts' after restarting terminal[/yellow]")


def install_bun():
    curl_install("https://bun.sh/install")


def install_uv():
    curl_sh_install("https://astral.sh/uv/install.sh")


def install_conda():
    if OS == "macos":
        arch = "arm64" if platform.machine() == "arm64" else "x86_64"
        url = f"https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-{arch}.sh"
    else:
        url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    run(f"curl -fsSL {url} -o /tmp/miniconda.sh && bash /tmp/miniconda.sh -b && rm /tmp/miniconda.sh")
    console.print("[yellow]Run 'conda init' after restarting terminal[/yellow]")


def install_starship():
    curl_sh_install("https://starship.rs/install.sh", "-y")
    console.print('[yellow]Add to shell: eval "$(starship init bash)" or eval "$(starship init zsh)"[/yellow]')


def install_1password_cli():
    if OS == "macos":
        run("brew install --cask 1password-cli")
    else:
        run("""curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg && \
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/amd64 stable main" | \
sudo tee /etc/apt/sources.list.d/1password.list && \
sudo apt-get update && sudo apt-get install -y 1password-cli""")


def install_claude():
    npm_install("@anthropic-ai/claude-code")


def install_codex():
    npm_install("@openai/codex")


def install_opencode():
    npm_install("opencode-ai")


def install_openspec():
    npm_install("openspec-ai")


def install_oh_my_opencode():
    run("npx oh-my-opencode install")


def install_vibe_kanban():
    run("npx vibe-kanban")


# ============================================================
# Software Registry
# ============================================================

SOFTWARE: list[Software] = [
    # Base Tools
    Software("Homebrew", "brew", install_homebrew, "base"),
    Software("Git", "git", install_git, "base"),
    Software("Tmux", "tmux", install_tmux, "base"),
    Software("Node.js", "node", install_nodejs, "base"),
    Software("Bun", "bun", install_bun, "base"),
    Software("uv", "uv", install_uv, "base"),
    Software("Conda", "conda", install_conda, "base"),
    Software("Starship", "starship", install_starship, "base"),
    Software("1Password CLI", "op", install_1password_cli, "base"),
    # Vibe Coding
    Software("Claude Code", "claude", install_claude, "vibe"),
    Software("Codex", "codex", install_codex, "vibe"),
    Software("opencode-ai", "opencode", install_opencode, "vibe"),
    Software("openspec", "openspec", install_openspec, "vibe"),
    Software("oh-my-opencode", None, install_oh_my_opencode, "vibe"),
    Software("vibe-kanban", None, install_vibe_kanban, "vibe"),
]

# ============================================================
# UI
# ============================================================

selected: list[bool] = [False] * len(SOFTWARE)


def get_indices_by_category(category: str) -> list[int]:
    return [i for i, s in enumerate(SOFTWARE) if s.category == category]


def show_menu():
    console.clear()
    console.print(Panel.fit("[bold cyan]sdpkjc.env Installer[/bold cyan]", box=box.DOUBLE))
    console.print()

    for category, title in [("base", "Base Tools"), ("vibe", "Vibe Coding")]:
        table = Table(title=f"[bold]{title}[/bold]", box=box.ROUNDED, show_header=False)
        table.add_column("Sel", width=3)
        table.add_column("No", width=3)
        table.add_column("Name", width=15)
        table.add_column("Status", width=12)

        for i in get_indices_by_category(category):
            sw = SOFTWARE[i]
            check = "[green]x[/green]" if selected[i] else " "
            if sw.check_cmd is None:
                status = "[dim]npx[/dim]"
            elif sw.is_installed():
                status = "[green]installed[/green]"
            else:
                status = "[yellow]missing[/yellow]"
            table.add_row(f"[{check}]", str(i + 1), sw.name, status)

        console.print(table)
        console.print()

    console.print("[bold]Quick Select:[/bold]")
    console.print("  [bold]a[/bold] - Base tools    [bold]v[/bold] - Vibe coding    [bold]A[/bold] - All")
    console.print("  [bold]c[/bold] - Clear         [bold]m[/bold] - Missing only")
    console.print()
    console.print("[dim]Numbers=toggle, Enter=install, q=quit[/dim]")
    console.print()


def install_selected():
    count = sum(selected)
    if count == 0:
        console.print("[yellow]Nothing selected![/yellow]")
        return

    console.print(f"\n[cyan]Installing {count} item(s)...[/cyan]\n")

    for i, sel in enumerate(selected):
        if sel:
            console.print(f"[bold]>>> {SOFTWARE[i].name}[/bold]")
            SOFTWARE[i].run_install()
            console.print()

    console.print("[bold green]Done![/bold green]")
    Prompt.ask("Press Enter to continue")


def main():
    global selected
    n = len(SOFTWARE)
    base_indices = get_indices_by_category("base")
    vibe_indices = get_indices_by_category("vibe")

    while True:
        show_menu()
        choice = Prompt.ask("Choice", default="")

        if choice.isdigit() and 1 <= int(choice) <= n:
            idx = int(choice) - 1
            selected[idx] = not selected[idx]
        elif choice == "a":
            for i in base_indices:
                selected[i] = True
        elif choice == "v":
            for i in vibe_indices:
                selected[i] = True
        elif choice == "A":
            selected = [True] * n
        elif choice == "c":
            selected = [False] * n
        elif choice == "m":
            for i, sw in enumerate(SOFTWARE):
                if not sw.is_installed():
                    selected[i] = True
        elif choice == "":
            install_selected()
        elif choice.lower() == "q":
            console.print("[green]Bye![/green]")
            break


if __name__ == "__main__":
    main()
