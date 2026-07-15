#!/usr/bin/env python3
"""
Injects agent and skill content into installer.py.
"""
import pathlib

def main():
    agent = pathlib.Path('md/tastar.md').read_text(encoding='utf-8')
    skill = pathlib.Path('md/tastar/SKILL.md').read_text(encoding='utf-8')
    installer = pathlib.Path('installer.py').read_text(encoding='utf-8')

    # Escape backslashes and double quotes for safe embedding in Python string
    agent_escaped = agent.replace('\\', '\\\\').replace('"', '\\"')
    skill_escaped = skill.replace('\\', '\\\\').replace('"', '\\"')

    installer = installer.replace('{{AGENT_CONTENT}}', agent_escaped)
    installer = installer.replace('{{SKILL_CONTENT}}', skill_escaped)

    pathlib.Path('installer.py').write_text(installer, encoding='utf-8')
    print("Injection successful.")

if __name__ == "__main__":
    main()