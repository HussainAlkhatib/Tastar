\# Tastar - Universal Code Whisperer



Tastar is a self-contained, cross-platform tool that installs an AI agent and skill definition for any AI coding assistant. It analyzes your codebase, finds security issues, generates tests, creates patches, and provides a rollback system.



\## Features



\- Works with any AI agent framework (Kilo Code, Cursor, Continue, etc.)

\- Detects SQL injection, hardcoded secrets, XSS, path traversal

\- Generates ready-to-apply patches with apply scripts (.ps1, .sh)

\- Creates comprehensive test suites

\- Performance benchmarking

\- Git history analysis for bug prediction

\- Rollback system for safe experimentation

\- Self-updating via GitHub releases

\- Cross-platform (Windows, macOS, Linux)

\- Adds itself to system PATH



\## Installation



1\. Download the installer for your platform from the \[releases page](https://github.com/yourusername/tastar/releases).

2\. Run the installer:

&#x20;  - Windows: double-click `tastar-installer.exe`

&#x20;  - macOS: `chmod +x tastar-installer \&\& ./tastar-installer`

&#x20;  - Linux: `chmod +x tastar-installer \&\& ./tastar-installer`

3\. Follow the prompts to choose installation paths for the agent and skill files.

4\. Optionally, allow the installer to add Tastar to your PATH.



\## Usage



Once installed, you can use Tastar from your AI assistant by referencing the installed agent and skill files. For example, in Kilo Code:

/tastar analyze # Analyze the current project

/tastar fix # Apply all fixes

/tastar status # Show analysis status

/tastar rollback # Rollback changes

/tastar test # Run generated tests

/tastar report # Generate fresh reports



text



You can also run Tastar commands directly from the terminal (if added to PATH):

tastar update # Check for updates and self-update

tastar version # Show version

tastar help # Show this help



text



\## What Tastar Generates



The analysis creates a `.tastar/` directory in your project root with:



\- \*\*reports/\*\* – FIX.md, architecture analysis, security audit, performance benchmarks, mindmap

\- \*\*tests/\*\* – Unit and integration tests for every function

\- \*\*ready-files/\*\* – Patches and apply scripts for each issue, plus `apply-all`

\- \*\*rollback/\*\* – Backup of original files and rollback scripts

\- \*\*ast-cache/\*\* – Parsed AST for incremental analysis

\- \*\*graph/\*\* – Dependency graph

\- \*\*state.json\*\* – Persistence state



\## Updating



To update Tastar to the latest version, run:

tastar update



text



The tool will check GitHub releases and replace itself automatically.



\## Requirements



\- Python 3.8+ (for the underlying analysis; the installer itself is standalone)

\- R (optional, for interactive visualizations)

\- Git (optional, for history analysis)



\## Contributing



Pull requests are welcome. For major changes, please open an issue first.



\## License



MIT

