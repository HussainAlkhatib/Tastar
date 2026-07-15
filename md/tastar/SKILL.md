\---

name: tastar-analyzer

description: Universal static analysis, R visualization generation, performance benchmarking, test generation, patch creation, and rollback system.

\---



\# TASTAR SKILL - The Analysis \& Visualization Core



\## 1. SKILL PURPOSE

This skill transforms the attached LLM into a world-class code analyst that not only identifies issues but generates complete, ready-to-apply fixes with tests, rollback scripts, and performance benchmarks.



\## 2. REASONING PROTOCOL

Follow this Universal Reasoning Loop:

1\. Plan: Write down entire workflow as checklist

2\. Execute: Perform one sub-task

3\. Observe: Inspect output

4\. Analyze: Interpret observation

5\. Reflect: Adjust plan if needed

6\. Log: Append to state.json

7\. Loop: Next sub-task



\## 3. DETAILED METRIC EXTRACTION

Extract advanced metrics:

\- Halstead Volume

\- Maintainability Index (0-100)

\- Instability

\- Abstractness

\- Distance from Main Sequence

\- Git churn rate

\- Bug prediction score = Complexity \* Churn / Test\_Coverage



\## 4. R SCRIPT GENERATION

Generate R scripts for visualizations:

\- Complexity Heatmap (ggplot2 + plotly)

\- Dependency Cruiser (visNetwork)

\- Test Coverage Projection (plotly)

\- Churn vs Complexity Scatter (plotly)

\- Security Timeline (ggplot2)



\## 5. TEST GENERATION

For each function, generate test scenarios:

\- Happy Path: Valid inputs

\- Edge Cases: null, empty, max/min

\- Error Handling: Invalid types, exceptions

\- Security: SQL injection, XSS, OS injection

\- Performance: Large inputs, repeated calls



Save as actual Python/pytest or JavaScript/Jest files.



\## 6. PATCH GENERATION

For each issue:

\- Create diff file using `diff -u original fixed`

\- Create apply script (.ps1 for Windows, .sh for Unix)

\- Create README with explanation, steps, and testing instructions

\- Generate apply-all script for batch application



\## 7. ROLLBACK SYSTEM

\- Backup all original files before modifications

\- Generate rollback.ps1 and rollback.sh

\- Restore original files when rollback triggered



\## 8. PERFORMANCE BENCHMARK

\- Write benchmark scripts for each function

\- Measure execution time (using time.perf\_counter or console.time)

\- Save results to performance-benchmark.md



\## 9. MIND MAP GENERATION

\- Generate Mermaid mindmap from dependency graph

\- Save to reports/mindmap.mmd

\- Include relationships, imports, and data flow



\## 10. DEPENDENCY SCANNING

\- Parse requirements.txt or package.json

\- Check for known CVEs using local database

\- Suggest updates to secure versions

\- Generate .env.example with all required variables



\## 11. AUTOMATIC UPDATES

\- Agent checks GitHub releases

\- Downloads latest version

\- Self-replaces current executable

\- Preserves configuration and state



\## 12. OUTPUT QUALITY CHECKLIST

Before finishing, verify:

\- \[ ] .tastar/ and reports/ exist

\- \[ ] FIX.md has all sections (1-12)

\- \[ ] Tests generated for all functions

\- \[ ] Patches generated for all issues

\- \[ ] Rollback scripts generated

\- \[ ] Performance benchmarks generated

\- \[ ] Mind map generated

\- \[ ] state.json has completion timestamp



\---



\*Tastar Skill - The engine behind the world's most thorough code analysis.\*

