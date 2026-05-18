# ProfitPilot — 3-Minute Presentation Script (Rewritten)

## Before You Start

- Run `profitpilot.py` and have the app window open and visible
- Do NOT pre-load the demo — you will click `Load Campus Demo` live during the presentation
- The app should open clean with no products loaded

---

## 0:00–0:20 — Opening Hook

Smile. Look at the audience.

Say:

> "Hi everyone. Popular doesn't always mean profitable. ProfitPilot is a campus business simulator that helps you figure out the difference — before you spend real money finding out the hard way."

Pause one second.

> "I'll show you how it works in under three minutes."

---

## 0:20–0:40 — Load Demo and Dashboard

Click **Load Campus Demo**.

The product table fills instantly with 9 products.

Point to the dashboard cards at the top.

Say:

> "One click loads nine campus products — matcha, bubble tea, hoodies, snack boxes, and more. The dashboard immediately shows total revenue, total profit, and the current top product."

Point to the score column in the table.

Say:

> "Every product gets a score out of 100. That score isn't just based on sales — it's a weighted formula combining 40% profit, 40% margin, and 20% demand. So two products with the same revenue can score very differently."

---

## 0:40–1:10 — Product Snapshot (Best Product)

Click on **Iced Matcha Latte** in the table to select it.

Click **Product Snapshot**.

Say:

> "For any product, ProfitPilot calculates revenue, total cost, profit, margin, score, and gives a decision — High Potential, Good Performer, Needs Improvement, or At Risk."

Point to the recommendation text.

Say:

> "The recommendation explains the decision in plain language — not just a number. This is what makes it useful for someone who understands their products but not necessarily the business side."

---

## 1:10–1:35 — Sticker Pack (The Risk Example)

Click on **Welcome Week Sticker Pack** in the table.

Click **Product Snapshot**.

Slow down here. Let the result speak.

Say:

> "Now here's the most important example. The sticker pack has the highest demand of all nine products — 80 units. But look at the score: At Risk."

Point to the margin and profit.

Say:

> "The selling price is only 20 cents above cost. Students buy it constantly, but each sale barely earns anything. This is exactly why ProfitPilot exists — popular does not always mean profitable."

---

## 1:35–2:05 — Test Scenario (Fix Before Applying)

Keep **Welcome Week Sticker Pack** selected.

Click **Test Scenario**.

Enter:
- New Selling Price: `4.00`
- New Quantity: `80`

Click **Test Scenario**.

Say:

> "Instead of guessing, I can test a fix first — raise the price to $4, keep the same demand — and ProfitPilot shows me the new profit, margin, score, and decision before I commit to anything."

Point to the scenario result.

Say:

> "The score jumps and the decision changes. Now I can make a confident decision."

Click **Apply Tested Scenario**.

Say:

> "Once I'm happy with the result, I apply it. The table, dashboard, and score all update automatically."

---

## 2:05–2:25 — Business Summary

Click **Business Summary**.

Say:

> "The Business Summary gives the full picture — total revenue, total profit, average score, best product, weakest product, and a ranked list with suggested actions for each."

Pause briefly.

Say:

> "The ranking is built using a recursive function — each product is inserted in score order through recursive calls. It's a small detail, but it shows the logic is built properly, not just patched together."

---

## 2:25–2:45 — Break-Even Plan

Click **Break-Even Plan**.

Enter a fixed cost of `500`.

Click **Calculate Break-Even**.

Say:

> "The break-even planner estimates how many total units need to be sold to cover fixed costs — ingredients, packaging, a market stall fee. It uses the whole product mix together, so if the margins are too weak across all products, it tells you break-even is not possible with the current setup."

---

## 2:45–3:00 — Export and Close

Close the break-even window.

Click **Export Business Report**.

Say:

> "Finally, ProfitPilot exports a plain text report and a styled HTML report that opens automatically in the browser — ready to present, print, or save as PDF."

End with:

> "My goal was simple — turn a product list into real business decisions that actually make sense to someone running a small hustle."

Smile. Done.

---

## If Someone Asks To Add a Product Live

Say:

> "Sure — give me a name, cost, selling price, and expected quantity."

Use this if nobody suggests one:

| Field | Value |
|---|---|
| Product Name | Cookie |
| Cost Price | 1.20 |
| Selling Price | 3.50 |
| Expected Quantity | 25 |

Click **Add Product**, select it, click **Product Snapshot**.

Say:

> "Quantity here means expected demand — how many I think I can sell in a week or at an event."

---

## If a Tutor Asks About the Code

> "The project is split into five modules. `logic.py` handles all the calculations — revenue, profit, margin, score, what-if analysis, break-even, and recursive ranking. `profitpilot.py` is the Tkinter GUI and button callbacks. `storage.py` handles JSON save and load. `validators.py` parses and validates user input. `reports.py` generates the text and HTML exports. `test_profitpilot.py` runs seven unit tests against the calculation logic — all separate from the GUI so they can be tested cleanly."

Key functions to mention if asked:

- `calculate_metrics()` — runs the full pipeline: revenue, cost, profit, margin, score, decision, recommendation
- `calculate_score()` — weighted scoring: 40% profit, 40% margin, 20% demand
- `what_if_analysis()` — simulates changes without touching saved data, uses a deep copy of the product list
- `rank_products_recursive()` — inserts products in score order using recursion
- `business_break_even()` — weighted average contribution per unit across all products
- `export_business_reports()` — writes `.txt` and `.html` reports, HTML opens automatically via `webbrowser.open_new_tab()`

Unit tests:

```bash
python -m unittest test_profitpilot.py
```

Expected:
```
Ran 7 tests in 0.XXXs
OK
```

---

## Timing Guide

| Section | Time |
|---|---|
| Opening hook | 0:00–0:20 |
| Load demo + dashboard | 0:20–0:40 |
| Product Snapshot (Matcha) | 0:40–1:10 |
| Sticker Pack risk example | 1:10–1:35 |
| Test Scenario + Apply | 1:35–2:05 |
| Business Summary | 2:05–2:25 |
| Break-Even Plan | 2:25–2:45 |
| Export + Close | 2:45–3:00 |
