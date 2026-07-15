#!/usr/bin/env python3
"""
Tastar Installer - Self-contained executable
Installs Tastar Agent and Skill files, and optionally adds itself to PATH.
Supports update via GitHub releases.
"""
import os
import sys
import shutil
import subprocess
import json
import tempfile
import zipfile
import platform
from pathlib import Path
from datetime import datetime

VERSION = "1.0.0"
GITHUB_REPO = "yourusername/tastar"  # CHANGE THIS
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# Embedded file contents (these will be bundled by PyInstaller)
AGENT_CONTENT = """---
name: tastar
description: Supreme Code Architect & Autonomous Analyst.
tools:
  read_file: true
  write_file: true
  run_command: true
  search_files: true
  list_directory: true
---

# TASTAR AGENT - Universal Code Whisperer

... (full content as provided earlier)
"""

SKILL_CONTENT = """---
name: tastar-analyzer
description: Universal static analysis, patch generation, rollback.
---

# TASTAR SKILL - Analysis & Visualization Core

... (full content)
"""


def print_header():
    print("=" * 60)
    print(f"Tastar Installer v{VERSION}")
    print("=" * 60)
    print()


def get_input(prompt, default=""):
    try:
        if default:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        value = input(prompt).strip()
        return value if value else default
    except (EOFError, KeyboardInterrupt):
        print("\nInstallation cancelled.")
        sys.exit(1)


def get_default_paths():
    system = platform.system()
    if system == "Windows":
        agent_default = os.path.expanduser("~/.config/kilo/agents")
        skill_default = os.path.expanduser("~/.kilo/skills")
    elif system == "Darwin":
        agent_default = os.path.expanduser("~/.config/kilo/agents")
        skill_default = os.path.expanduser("~/.kilo/skills")
    else:  # Linux
        agent_default = os.path.expanduser("~/.config/kilo/agents")
        skill_default = os.path.expanduser("~/.kilo/skills")
    return agent_default, skill_default


def install_files(agent_path, skill_path):
    print("\nInstalling Tastar Agent...")
    agent_file = Path(agent_path) / "tastar.md"
    agent_file.parent.mkdir(parents=True, exist_ok=True)
    with open(agent_file, "w", encoding="utf-8") as f:
        f.write(AGENT_CONTENT)
    print(f"[OK] Agent installed to: {agent_file}")

    print("Installing Tastar Skill...")
    skill_dir = Path(skill_path) / "tastar"
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(SKILL_CONTENT)
    print(f"[OK] Skill installed to: {skill_file}")

    print("\n[SUCCESS] Tastar installed successfully!")


def add_to_path(executable_path):
    """Add the directory containing the executable to the system PATH."""
    system = platform.system()
    bin_dir = Path(executable_path).parent.resolve()
    if system == "Windows":
        # Use setx to add to user PATH
        current_path = os.environ.get("PATH", "")
        if str(bin_dir) not in current_path.split(os.pathsep):
            try:
                subprocess.run(
                    f'setx PATH "%PATH%;{bin_dir}"',
                    shell=True,
                    check=True,
                    capture_output=True,
                )
                print(f"[OK] Added {bin_dir} to user PATH. Please restart your terminal.")
            except subprocess.CalledProcessError:
                print("[ERROR] Could not add to PATH. You may need to run as Administrator.")
        else:
            print(f"[OK] {bin_dir} already in PATH.")
    else:
        # Unix-like: add to ~/.profile or ~/.bashrc
        shell_rc = os.path.expanduser("~/.profile")
        if platform.system() == "Darwin":
            # macOS might use .zshrc
            shell_rc = os.path.expanduser("~/.zshrc")
        if not os.path.exists(shell_rc):
            shell_rc = os.path.expanduser("~/.bashrc")
        with open(shell_rc, "a") as f:
            f.write(f'\nexport PATH="$PATH:{bin_dir}"\n')
        print(f"[OK] Added {bin_dir} to PATH in {shell_rc}.")
        print("Please restart your terminal or run 'source ~/.profile'.")


def main_install():
    print_header()
    print("This installer will set up Tastar for your AI coding assistant.")
    print("It works with any agent framework that uses .md files.")
    print()
    agent_default, skill_default = get_default_paths()
    print(f"Default Agent path: {agent_default}")
    print(f"Default Skill path: {skill_default}")
    print()

    agent_path = get_input("Agent installation path", agent_default)
    skill_path = get_input("Skill installation path", skill_default)

    if not agent_path or not skill_path:
        print("Error: Paths cannot be empty.")
        sys.exit(1)

    confirm = get_input(
        f"\nInstall to:\n  Agent: {agent_path}\n  Skill: {skill_path}\nConfirm? (yes/no)",
        "yes",
    )
    if confirm.lower() not in ("yes", "y"):
        print("Installation cancelled.")
        sys.exit(0)

    install_files(agent_path, skill_path)

    # Ask to add to PATH
    if get_input("Add Tastar executable to system PATH? (yes/no)", "yes").lower() in (
        "yes",
        "y",
    ):
        add_to_path(sys.argv[0])

    print("\nTastar is ready!")
    print("To use it inside your AI assistant, refer to the agent and skill files.")
    print("If you have a compatible agent framework (like Kilo Code), you can run:")
    print("  /tastar analyze")
    print("  /tastar fix")
    print("  /tastar status")
    print("  /tastar rollback")


def check_for_updates():
    print("Checking for updates...")
    try:
        import requests
        response = requests.get(GITHUB_API_URL, timeout=10)
        if response.status_code == 200:
            release = response.json()
            latest_tag = release.get("tag_name", "").replace("v", "")
            if latest_tag and latest_tag > VERSION:
                print(f"New version available: v{latest_tag} (current: v{VERSION})")
                ans = get_input("Update Tastar? (yes/no)", "yes")
                if ans.lower() in ("yes", "y"):
                    download_and_update(release)
                else:
                    print("Update skipped.")
            else:
                print(f"Tastar is up to date (v{VERSION})")
        else:
            print("Could not check for updates (GitHub API error).")
    except ImportError:
        print("Requests library not installed. Please install requests to enable updates.")
    except Exception as e:
        print(f"Update check failed: {e}")


def download_and_update(release):
    print("Downloading latest release...")
    for asset in release.get("assets", []):
        # Determine appropriate asset based on platform
        system = platform.system()
        if system == "Windows" and asset["name"].endswith(".exe"):
            url = asset["browser_download_url"]
        elif system == "Darwin" and asset["name"].endswith("mac"):
            url = asset["browser_download_url"]
        elif system == "Linux" and asset["name"].endswith("lin"):
            url = asset["browser_download_url"]
        else:
            continue
        try:
            import requests
            with tempfile.NamedTemporaryFile(delete=False, suffix=".exe" if system == "Windows" else "") as tmp:
                response = requests.get(url, stream=True)
                for chunk in response.iter_content(chunk_size=8192):
                    tmp.write(chunk)
                tmp_path = tmp.name

            # Replace current executable
            current_exe = Path(sys.argv[0])
            if system == "Windows":
                # Need to rename current exe to a backup, then copy new
                backup = current_exe.with_suffix(".exe.bak")
                shutil.move(current_exe, backup)
                shutil.copy2(tmp_path, current_exe)
                os.chmod(current_exe, 0o755)
                print("[OK] Tastar updated successfully!")
                print("The previous version was backed up as", backup)
            else:
                # Unix: overwrite
                shutil.copy2(tmp_path, current_exe)
                os.chmod(current_exe, 0o755)
                print("[OK] Tastar updated successfully!")
            os.unlink(tmp_path)
            sys.exit(0)
        except Exception as e:
            print(f"Update failed: {e}")
            sys.exit(1)
    else:
        print("No matching asset found for this platform.")


def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "update":
            check_for_updates()
            return
        elif cmd in ("--help", "-h", "help"):
            print("Tastar Installer and CLI")
            print("Usage: tastar [command]")
            print("Commands:")
            print("  update          Update Tastar to the latest version")
            print("  analyze         Run analysis (via your AI assistant)")
            print("  fix             Apply fixes (via your AI assistant)")
            print("  status          Show status (via your AI assistant)")
            print("  rollback        Rollback changes (via your AI assistant)")
            print("  test            Run tests (via your AI assistant)")
            print("  report          Generate reports (via your AI assistant)")
            print("  init            Create .tastar structure (via your AI assistant)")
            print("  clean           Remove .tastar files (via your AI assistant)")
            print("  version         Show version")
            print("  help            Show this help")
            print()
            print("Options: (for internal use)")
            print("  --path <dir>    Specify project path")
            print("  --force         Skip confirmations")
            print("  --verbose       Verbose output")
            return
        elif cmd == "version":
            print(f"Tastar v{VERSION}")
            return
        else:
            # Delegate to the agent; for now print a message
            print(f"Command '{cmd}' is intended to be run inside your AI assistant.")
            print("Please use the appropriate agent command (e.g., /tastar {cmd})")
            return

    # No command: run installer
    main_install()


if __name__ == "__main__":
    main()