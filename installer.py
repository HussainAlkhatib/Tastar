#!/usr/bin/env python3
import os, sys, shutil, subprocess, json, platform
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
    home = str(Path.home())
    if platform.system() == "Windows":
        return (os.path.join(home, ".config", "kilo", "agents"),
                os.path.join(home, ".kilo", "skills"))
    else:
        return (os.path.join(home, ".config", "kilo", "agents"),
                os.path.join(home, ".kilo", "skills"))

def save_paths(agent_path, skill_path):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"agent_path": agent_path, "skill_path": skill_path}, f)

def install_files(agent_path, skill_path):
    print("\nInstalling Tastar Agent...")
    agent_file = Path(agent_path) / "tastar.md"
    agent_file.parent.mkdir(parents=True, exist_ok=True)
    agent_file.write_text(AGENT_CONTENT, encoding="utf-8")
    print(f"[OK] Agent installed to: {agent_file}")

    print("Installing Tastar Skill...")
    skill_dir = Path(skill_path) / "tastar"
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(SKILL_CONTENT, encoding="utf-8")
    print(f"[OK] Skill installed to: {skill_file}")

    save_paths(str(agent_path), str(skill_path))
    print("\n[SUCCESS] Tastar installed successfully!")

def get_install_dir():
    system = platform.system()
    if system == "Windows":
        # Use Program Files (requires admin)
        prog_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        return Path(prog_files) / "Tastar"
    elif system == "Darwin":
        # Use /usr/local/bin (or ~/.local/bin)
        return Path("/usr/local/bin")
    else: # Linux
        return Path("/usr/local/bin")

def install_executable():
    """Copy the current executable to a permanent location and add to PATH."""
    current_exe = Path(sys.argv[0]).resolve()
    target_dir = get_install_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    # Determine target filename
    if platform.system() == "Windows":
        target_exe = target_dir / "tastar.exe"
    else:
        target_exe = target_dir / "tastar"

    print(f"\nCopying executable to: {target_exe}")
    try:
        shutil.copy2(current_exe, target_exe)
        if platform.system() != "Windows":
            os.chmod(target_exe, 0o755)
        print("[OK] Executable installed.")
    except Exception as e:
        print(f"[ERROR] Could not copy executable: {e}")
        return False

    # Add to PATH
    add_to_path(str(target_dir))
    return True

def add_to_path(bin_dir):
    system = platform.system()
    if system == "Windows":
        try:
            subprocess.run(
                f'setx /M PATH "%PATH%;{bin_dir}"',
                shell=True, check=True, capture_output=True
            )
            print(f"[OK] Added {bin_dir} to system PATH. Please restart your terminal.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Could not add to system PATH: {e.stderr.decode().strip()}")
            print("Please run the installer as Administrator.")
    elif system == "Darwin" or system == "Linux":
        # Try system-wide /etc/paths with sudo, fallback to user profile
        try:
            subprocess.run(
                f'echo "{bin_dir}" | sudo tee -a /etc/paths',
                shell=True, check=True, capture_output=True
            )
            print(f"[OK] Added {bin_dir} to system PATH via /etc/paths.")
        except:
            # Fallback to user profile
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
        if install_executable():
            print("\nTastar is now available globally as 'tastar'.")
        else:
            print("\nCould not install executable. You can manually add the directory to PATH.")

    print("\nTo use Tastar inside your AI assistant, refer to the agent and skill files.")
    print("If you have a compatible agent framework, you can run commands like:")
    print("  /tastar analyze")
    print("  /tastar fix")
    print("\nAdditional CLI commands:")
    print("  tastar delete          - Remove installed files")
    print("  tastar delete --self   - Also remove the executable")
    print("  tastar update          - Self-update (coming soon)")

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