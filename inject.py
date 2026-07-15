#!/usr/bin/env python3
"""
Inject agent and skill content into installer.py
"""
import pathlib

def main():
    agent_path = pathlib.Path('md/tastar.md')
    skill_path = pathlib.Path('md/tastar/SKILL.md')
    installer_path = pathlib.Path('installer.py')

    if not agent_path.exists():
        print(f"Error: {agent_path} not found")
        return 1
    if not skill_path.exists():
        print(f"Error: {skill_path} not found")
        return 1

    agent_content = agent_path.read_text(encoding='utf-8')
    skill_content = skill_path.read_text(encoding='utf-8')

    # Escape backslashes and quotes for embedding in Python string
    agent_escaped = agent_content.replace('\\', '\\\\').replace('"', '\\"')
    skill_escaped = skill_content.replace('\\', '\\\\').replace('"', '\\"')

    installer = installer_path.read_text(encoding='utf-8')
    installer = installer.replace('{{AGENT_CONTENT}}', agent_escaped)
    installer = installer.replace('{{SKILL_CONTENT}}', skill_escaped)
    installer_path.write_text(installer, encoding='utf-8')

    print("Injection successful.")
    return 0

if __name__ == "__main__":
    exit(main())