#!/usr/bin/env python3
"""
Tastar Installer - Self-contained executable
Installs Tastar executable to a dedicated folder, adds to PATH,
and installs Agent/Skill files.
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
    print("="*60)
    print(f"Tastar Installer v{VERSION}")
    print("="*60)
    print()

def get_input(prompt, default=""):
    try:
        if default:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        value = input(prompt).strip()
        return value if value else default
    except:
        print("\nInstallation cancelled.")
        sys.exit(1)

def get_default_paths():
    system = platform.system()
    home = str(Path.home())
    if system == "Windows":
        bin_default = "C:\\tastar"
        agent_default = os.path.join(home, ".config", "kilo", "agents")
        skill_default = os.path.join(home, ".kilo", "skills")
    else:
        bin_default = "/opt/tastar"
        agent_default = os.path.join(home, ".config", "kilo", "agents")
        skill_default = os.path.join(home, ".kilo", "skills")
    return bin_default, agent_default, skill_default

def save_paths(bin_path, agent_path, skill_path):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({
            "bin_path": bin_path,
            "agent_path": agent_path,
            "skill_path": skill_path
        }, f)

def install_files(bin_path, agent_path, skill_path):
    # 1. Install executable to its own folder
    print("\nInstalling Tastar executable...")
    bin_dir = Path(bin_path)
    bin_dir.mkdir(parents=True, exist_ok=True)
    current_exe = Path(sys.argv[0]).resolve()
    target_exe = bin_dir / current_exe.name
    shutil.copy2(current_exe, target_exe)
    if platform.system() != "Windows":
        target_exe.chmod(0o755)
    print(f"[OK] Executable installed to: {target_exe}")

    # 2. Install Agent
    print("Installing Tastar Agent...")
    agent_file = Path(agent_path) / "tastar.md"
    agent_file.parent.mkdir(parents=True, exist_ok=True)
    agent_file.write_text(AGENT_CONTENT, encoding="utf-8")
    print(f"[OK] Agent installed to: {agent_file}")

    # 3. Install Skill
    print("Installing Tastar Skill...")
    skill_dir = Path(skill_path) / "tastar"
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(SKILL_CONTENT, encoding="utf-8")
    print(f"[OK] Skill installed to: {skill_file}")

    save_paths(str(bin_path), str(agent_path), str(skill_path))
    print("\n[SUCCESS] Tastar installed successfully!")

def add_to_path(bin_path):
    system = platform.system()
    bin_dir = Path(bin_path).resolve()
    if system == "Windows":
        try:
            # Since we have admin rights (--uac-admin), use /M for system PATH
            subprocess.run(
                f'setx /M PATH "%PATH%;{bin_dir}"',
                shell=True, check=True, capture_output=True
            )
            print(f"[OK] Added {bin_dir} to system PATH. Please restart your terminal.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Could not add to system PATH: {e.stderr.decode().strip()}")
            print("Please run the installer as Administrator.")
    elif system == "Darwin" or system == "Linux":
        # Try system-wide via /etc/paths (requires sudo), fallback to user profile
        try:
            subprocess.run(
                f'echo "{bin_dir}" | sudo tee -a /etc/paths',
                shell=True, check=True, capture_output=True
            )
            print(f"[OK] Added {bin_dir} to system PATH via /etc/paths.")
        except:
            # Fallback to user's shell profile
            shell_rc = os.path.expanduser("~/.profile")
            if system == "Darwin":
                shell_rc = os.path.expanduser("~/.zshrc")
            if not os.path.exists(shell_rc):
                shell_rc = os.path.expanduser("~/.bashrc")
            with open(shell_rc, "a") as f:
                f.write(f'\nexport PATH="$PATH:{bin_dir}"\n')
            print(f"[OK] Added {bin_dir} to PATH in {shell_rc}.")
            print("Please restart your terminal or run 'source ~/.profile'.")
    else:
        print("Unsupported OS for PATH addition.")

def main_install():
    print_header()
    print("This installer sets up Tastar for your AI coding assistant.\n")

    bin_default, agent_default, skill_default = get_default_paths()
    bin_path = get_input("Where should Tastar executable be installed? (Path)", bin_default)
    agent_path = get_input("Im Tastar Agent, where can i go? (Path)", agent_default)
    skill_path = get_input("And i have a child, named Tastar Skill, where can he go? (Path)", skill_default)

    if not bin_path or not agent_path or not skill_path:
        print("Error: Paths cannot be empty.")
        sys.exit(1)

    print(f"\nExecutable will be installed to: {bin_path}")
    print(f"Agent will be installed to: {agent_path}")
    print(f"Skill will be installed to: {skill_path}")
    confirm = get_input("\nConfirm installation? (yes/no)", "yes")
    if confirm.lower() not in ("yes", "y"):
        print("Installation cancelled.")
        sys.exit(0)

    install_files(bin_path, agent_path, skill_path)

    if get_input("Add Tastar executable directory to system PATH? (yes/no)", "yes").lower() in ("yes", "y"):
        add_to_path(bin_path)

    print("\nTastar is ready!")
    print(f"You can now run 'tastar' from any terminal (after restarting).")
    print("To use it inside your AI assistant, refer to the agent and skill files.")
    print("Commands:")
    print("  tastar analyze          - Run analysis on current project")
    print("  tastar fix              - Apply all fixes")
    print("  tastar delete           - Remove installed files")
    print("  tastar delete --self    - Also remove this executable")
    print("  tastar update           - Self-update (coming soon)")

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd in ("--help", "-h", "help"):
            print("Tastar Installer and CLI")
            print("Usage: tastar [command]")
            print("Commands:")
            print("  update          Self-update (coming soon)")
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