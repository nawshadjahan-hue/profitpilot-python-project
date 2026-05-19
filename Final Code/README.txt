ProfitPilot - COMP9001 Final Project

Starting point:
Run profitpilot.py

Command:
python profitpilot.py

Optional test command:
python -m unittest test_profitpilot.py

Required libraries:
No extra installation is needed. The project only uses Python standard library
modules, including tkinter, json, math, html, webbrowser, and unittest.

Files:
profitpilot.py      - main Tkinter app and user interface
logic.py            - business calculations, scoring, recommendations, recursion
storage.py          - JSON save/load functions
validators.py       - input validation helpers
reports.py          - text and HTML report export
demo_data.py        - sample campus products for the demo button
test_profitpilot.py - unit tests for the calculation logic
products.json       - saved product data file, can be empty

How to use:
1. Run profitpilot.py.
2. Click Load Campus Demo to load sample products.
3. Select a product and click Product Snapshot.
4. Use Test Scenario or Break-Even Plan to explore business decisions.
5. Click Export Business Report to create report files.
