# ProfitPilot: Campus Business Simulator

ProfitPilot is a Tkinter desktop app for students who want to test whether a
campus side hustle can make profit. It helps users compare products, understand
profit and margin, test price or demand changes, estimate break-even sales, and
export a business report.

## Main Features

- Add, edit, delete, save, and load products
- Load sample campus demo products
- View product revenue, cost, profit, margin, score, and decision
- View an overall Business Summary
- Test what-if scenarios before applying changes
- Estimate break-even units for the whole product mix
- Exports plain text and HTML business reports

## Advanced Topics Used

- File I/O with JSON save/load and report export
- Exception handling for invalid inputs and file errors
- Recursion for ranking products in the business summary
- Unit testing with `unittest`
- GUI programming with Tkinter

## How To Run

Go to the `Final Code` folder and run:

```bash
python profitpilot.py
```

This is a Tkinter GUI application, so it should be run on a local computer with
a display. Online terminals such as ED may not open the window because they do
not provide a graphical display.

No extra installation is needed. The project only uses Python standard library
modules, including `tkinter`, `json`, `math`, `html`, `webbrowser`, and
`unittest`.

## How To Use

1. Run `profitpilot.py`.
2. Click **Load Campus Demo** to load sample products.
3. Select **Iced Matcha Latte** and click **Product Snapshot**.
4. Click **Business Summary** to view the overall business performance.
5. Select **Welcome Week Sticker Pack** and click **Test Scenario**.
   Example scenario: New Selling Price = `4.00`, New Quantity = `80`.
6. Click **Break-Even Plan**.
   Example fixed cost: `500`.
7. Click **Export Business Report** to create report files.

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
