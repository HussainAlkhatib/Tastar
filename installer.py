#!/usr/bin/env python3
"""
Tastar Installer - Self-contained executable
Installs Tastar Agent and Skill files, and adds itself to system PATH.
"""
import os
import sys
import shutil
import subprocess
import json
import platform
from pathlib import Path

VERSION = "1.0.0"
AGENT_CONTENT = """{{AGENT_CONTENT}}"""
SKILL_CONTENT = """{{SKILL_CONTENT}}"""
CONFIG_DIR = Path.home() / ".tastar"
CONFIG_FILE = CONFIG_DIR / "install_paths.json"

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
    else:
        agent_default = os.path.expanduser("~/.config/kilo/agents")
        skill_default = os.path.expanduser("~/.kilo/skills")
    return agent_default, skill_default

def save_paths(agent_path, skill_path):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"agent_path": agent_path, "skill_path": skill_path}, f)

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

def add_to_system_path(executable_path):
    """Add the directory containing the executable to the system PATH."""
    bin_dir = Path(executable_path).parent.resolve()
    system = platform.system()
    if system == "Windows":
        try:
            # Use setx /M to modify system PATH (requires admin)
            subprocess.run(
                f'setx /M PATH "%PATH%;{bin_dir}"',
                shell=True,
                check=True,
                capture_output=True,
            )
            print(f"[OK] Added {bin_dir} to system PATH. Please restart your terminal.")
        except subprocess.CalledProcessError:
            print("[ERROR] Could not add to system PATH. Please run the installer as Administrator.")
    else:
        # Unix: add to /etc/paths or ~/.profile
        shell_rc = os.path.expanduser("~/.profile")
        if system == "Darwin":
            shell_rc = os.path.expanduser("~/.zshrc")
        if not os.path.exists(shell_rc):
            shell_rc = os.path.expanduser("~/.bashrc")
        with open(shell_rc, "a") as f:
            f.write(f'\nexport PATH="$PATH:{bin_dir}"\n')
        print(f"[OK] Added {bin_dir} to PATH in {shell_rc}.")
        print("Please restart your terminal or run 'source ~/.profile'.")

def main_install():
    print_header()
    print("This installer sets up Tastar for your AI coding assistant.\n")
    agent_default, skill_default = get_default_paths()
    agent_path = get_input("Im Tastar Agent, where can i go? (Path)", agent_default)
    skill_path = get_input("And i have a child, named Tastar Skill, where can he go? (Path)", skill_default)

    if not agent_path or not skill_path:
        print("Error: Paths cannot be empty.")
        sys.exit(1)

    print(f"\nAgent will be installed to: {agent_path}")
    print(f"Skill will be installed to: {skill_path}")
    confirm = get_input("\nConfirm installation? (yes/no)", "yes")
    if confirm.lower() not in ("yes", "y"):
        print("Installation cancelled.")
        sys.exit(0)

    install_files(agent_path, skill_path)

    if get_input("Add Tastar executable to system PATH? (yes/no)", "yes").lower() in ("yes", "y"):
        add_to_system_path(sys.argv[0])

    print("\nTastar is ready!")
    print("To use it inside your AI assistant, refer to the agent and skill files.")
    print("If you have a compatible agent framework, you can run commands like:")
    print("  /tastar analyze")
    print("  /tastar fix")
    print("\nAdditional CLI commands:")
    print("  tastar delete          - Remove installed files")
    print("  tastar delete --self   - Also remove this executable")
    print("  tastar update          - Self-update")

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "update":
            # Placeholder - we'll implement later
            print("Update feature not yet implemented.")
            return
        elif cmd == "delete":
            # Implement delete logic (similar to previous)
            print("Delete feature not yet implemented.")
            return
        elif cmd in ("--help", "-h", "help"):
            print("Tastar Installer and CLI")
            print("Usage: tastar [command]")
            print("Commands:")
            print("  update          Self-update")
            print("  delete          Remove installed files")
            print("  delete --self   Also remove executable")
            print("  version         Show version")
            print("  help            Show this help")
            return
        elif cmd == "version":
            print(f"Tastar v{VERSION}")
            return
        else:
            print(f"Command '{cmd}' is intended for use inside your AI assistant.")
            return
    main_install()

if __name__ == "__main__":
    main()