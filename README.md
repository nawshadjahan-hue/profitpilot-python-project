# ProfitPilot: Campus Business Simulator

![ProfitPilot cover](profitpilot_cover_group_students_updated.png)

ProfitPilot is a Python desktop app that helps students test whether a small
campus side hustle can actually make money. Users can compare products, check
profit and margin, test what-if scenarios, estimate break-even sales, and export
a business report.

## What It Does

- Calculates revenue, total cost, profit, and profit margin
- Gives each product a ProfitPilot score out of 100
- Labels products as High Potential, Good Performer, Needs Improvement, or At Risk
- Tests price and demand changes before applying them
- Estimates break-even sales for the overall product mix
- Saves and loads product data
- Exports plain text and HTML business reports

## How To Run

Go to the `Final Code` folder and run:

```bash
python profitpilot.py
```

This is a Tkinter GUI application, so it should be run on a local computer with
a display. Online terminals such as ED may not open the window because they do
not provide a graphical display.

## How To Test

From the `Final Code` folder:

```bash
python -m unittest test_profitpilot.py
```

## Project Files

```text
Final Code/
  profitpilot.py      main Tkinter app and user interface
  logic.py            business calculations, scoring, recommendations, recursion
  storage.py          JSON save/load functions
  validators.py       input validation helpers
  reports.py          text and HTML report export
  demo_data.py        sample campus products for the demo button
  test_profitpilot.py unit tests for the calculation logic
  products.json       saved product data file, can be empty
```

## Built With

- Python
- Tkinter
- Python standard library modules only

