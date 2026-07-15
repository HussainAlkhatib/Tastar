#!/usr/bin/env python3
"""
Tastar Installer - Self-contained executable
Installs Tastar Agent and Skill files, and optionally adds itself to PATH.
Supports update via GitHub releases.
Supports delete/uninstall commands.
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
GITHUB_REPO = "HussainAlkhatib/Tastar"  # CHANGE THIS TO YOUR REPO
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# These placeholders will be replaced by inject.py
AGENT_CONTENT = """{{AGENT_CONTENT}}"""
SKILL_CONTENT = """{{SKILL_CONTENT}}"""

CONFIG_DIR = Path.home() / ".tastar"
CONFIG_FILE = CONFIG_DIR / "install_paths.json"


def print_header():
    print("=" * 60)
    print(f"Tastar v{VERSION}")
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
        print("\nOperation cancelled.")
        sys.exit(1)


def get_default_paths():
    system = platform.system()
    if system == "Windows":
        agent_default = os.path.expanduser("~/.config/kilo/agents")
        skill_default = os.path.expanduser("~/.kilo/skills")
    else:  # Unix-like
        agent_default = os.path.expanduser("~/.config/kilo/agents")
        skill_default = os.path.expanduser("~/.kilo/skills")
    return agent_default, skill_default


def save_paths(agent_path, skill_path):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"agent_path": agent_path, "skill_path": skill_path}, f)


def load_paths():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return None


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

    save_paths(str(agent_path), str(skill_path))
    print("\n[SUCCESS] Tastar installed successfully!")


def add_to_path(executable_path):
    """Add the directory containing the executable to the system PATH."""
    system = platform.system()
    bin_dir = Path(executable_path).parent.resolve()
    if system == "Windows":
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
        shell_rc = os.path.expanduser("~/.profile")
        if platform.system() == "Darwin":
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
    print("\nAdditional CLI commands:")
    print("  tastar delete          - Remove installed agent and skill files")
    print("  tastar delete --self   - Also remove this executable")


def cmd_delete(args):
    """Delete installed files."""
    paths = load_paths()
    if not paths:
        print("No installation record found. Run 'tastar' to install first.")
        return

    agent_path = Path(paths["agent_path"])
    skill_path = Path(paths["skill_path"])

    print("The following will be deleted:")
    print(f"  Agent: {agent_path / 'tastar.md'}")
    print(f"  Skill: {skill_path / 'tastar'}")
    if "--self" in args:
        print(f"  Executable: {sys.argv[0]} (this file)")

    confirm = get_input("Are you sure? (yes/no)", "no")
    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    # Delete agent file
    agent_file = agent_path / "tastar.md"
    if agent_file.exists():
        agent_file.unlink()
        print(f"[OK] Deleted {agent_file}")
    else:
        print(f"[SKIP] {agent_file} not found")

    # Delete skill folder
    skill_folder = skill_path / "tastar"
    if skill_folder.exists():
        shutil.rmtree(skill_folder)
        print(f"[OK] Deleted {skill_folder}")
    else:
        print(f"[SKIP] {skill_folder} not found")

    # Delete config
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
        print("[OK] Deleted installation record")
        # remove config dir if empty
        try:
            CONFIG_DIR.rmdir()
        except OSError:
            pass

    # Delete self if requested
    if "--self" in args:
        self_exe = Path(sys.argv[0]).resolve()
        if self_exe.exists():
            try:
                if platform.system() == "Windows":
                    # Cannot delete running exe; create a batch file to delete after exit
                    bat_path = self_exe.with_suffix(".bat")
                    with open(bat_path, "w") as f:
                        f.write(f'@echo off\n:loop\ntimeout /t 1 /nobreak >nul\ndel "{self_exe}"\nif exist "{self_exe}" goto loop\ndel "%~f0"\n')
                    print(f"[OK] Created {bat_path} to delete the executable after this process exits.")
                    print("Please run that batch file manually as Administrator if needed.")
                else:
                    # Unix: can delete after exit using a shell script
                    sh_path = self_exe.with_suffix(".sh")
                    with open(sh_path, "w") as f:
                        f.write(f'#!/bin/bash\nsleep 1\nrm -f "{self_exe}"\nrm -f "$0"\n')
                    os.chmod(sh_path, 0o755)
                    print(f"[OK] Created {sh_path} to delete the executable after this process exits.")
                    print("Run that script manually (e.g., ./delete.sh) to finalize removal.")
                print("Please also remove the directory containing this executable from your PATH if you added it.")
            except Exception as e:
                print(f"[ERROR] Could not create deletion script: {e}")
                print(f"Please delete '{self_exe}' manually.")

    print("\nTastar has been removed.")


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

            current_exe = Path(sys.argv[0])
            if system == "Windows":
                backup = current_exe.with_suffix(".exe.bak")
                shutil.move(current_exe, backup)
                shutil.copy2(tmp_path, current_exe)
                os.chmod(current_exe, 0o755)
                print("[OK] Tastar updated successfully!")
                print("The previous version was backed up as", backup)
            else:
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
        elif cmd == "delete":
            cmd_delete(sys.argv[2:])
            return
        elif cmd in ("--help", "-h", "help"):
            print("Tastar Installer and CLI")
            print("Usage: tastar [command]")
            print("Commands:")
            print("  update          Update Tastar to the latest version")
            print("  delete          Remove installed agent and skill files")
            print("  delete --self   Also remove the Tastar executable itself")
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
            print(f"Command '{cmd}' is intended to be run inside your AI assistant.")
            print("Please use the appropriate agent command (e.g., /tastar {cmd})")
            return

    # No command: run installer
    main_install()


if __name__ == "__main__":
    main()