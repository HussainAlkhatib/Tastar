#!/usr/bin/env python3
"""
Build script for Tastar installer executables.
Uses PyInstaller to create standalone executables for Windows, macOS, Linux.
"""
import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

VERSION = "1.0.0"
INSTALLER_SCRIPT = "installer.py"
OUTPUT_DIR = Path("dist")

def run_pyinstaller(platform_name, extra_args=None):
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--console",
        f"--name=tastar-installer-{platform_name}",
        "--add-data", f"README.md:.",
        INSTALLER_SCRIPT,
    ]
    if extra_args:
        cmd.extend(extra_args)
    subprocess.run(cmd, check=True)

def build():
    print("Building Tastar Installer executables...")
    OUTPUT_DIR.mkdir(exist_ok=True)

    system = platform.system()
    if system == "Windows":
        print("Building for Windows...")
        run_pyinstaller("win")
        exe = Path("dist/tastar-installer-win.exe")
        if exe.exists():
            target = OUTPUT_DIR / "win" / "tastar-installer.exe"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(exe), str(target))
            print(f"[OK] Windows executable: {target}")
    elif system == "Darwin":
        print("Building for macOS...")
        run_pyinstaller("mac")
        exe = Path("dist/tastar-installer-mac")
        if exe.exists():
            target = OUTPUT_DIR / "mac" / "tastar-installer"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(exe), str(target))
            os.chmod(target, 0o755)
            print(f"[OK] macOS executable: {target}")
    else:  # Linux
        print("Building for Linux...")
        run_pyinstaller("lin")
        exe = Path("dist/tastar-installer-lin")
        if exe.exists():
            target = OUTPUT_DIR / "lin" / "tastar-installer"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(exe), str(target))
            os.chmod(target, 0o755)
            print(f"[OK] Linux executable: {target}")

    print("\nBuild complete!")
    print("Executables are in the 'dist' directory.")
    print("To build for other platforms, run this script on those platforms.")
    print("Alternatively, use GitHub Actions (see workflow file).")

if __name__ == "__main__":
    if not shutil.which("pyinstaller"):
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    build()