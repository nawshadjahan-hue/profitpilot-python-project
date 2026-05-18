# ProfitPilot â€” 3-Minute Presentation Script (v3, tightened)

## Before You Start

- Run `profitpilot.py` and have the app window open and visible
- Do NOT pre-load the demo â€” you will click `Load Campus Demo` live
- The app should open clean with no products loaded
- Speak a touch slower than usual â€” clarity beats speed when people are voting

---

## 0:00â€“0:15 â€” Opening Hook

Smile. Look at the audience.

Say:

> "Hi everyone. Popular doesn't always mean profitable. ProfitPilot is a campus business simulator that shows you the difference â€” before you lose real money finding out. Let me show you."

---

## 0:15â€“0:35 â€” Load Demo and Dashboard

Click **Load Campus Demo**. The table fills with 9 products.

Point to the dashboard cards.

Say:

> "One click loads nine campus products. The dashboard instantly shows total revenue, total profit, and the top product."

Point to the score column.

Say:

> "Every product gets a score out of 100 â€” a weighted mix of 40% profit, 40% margin, and 20% demand. So two products with the same revenue can score very differently."

---

## 0:35â€“1:00 â€” Product Snapshot (Best Product)

Click **Iced Matcha Latte** â†’ click **Product Snapshot**.

Say:

> "For any product, ProfitPilot calculates revenue, cost, profit, margin, a score, and a decision â€” High Potential, Good Performer, Needs Improvement, or At Risk. The recommendation explains it in plain language, not just a number."

---

## 1:00â€“1:25 â€” Sticker Pack (The Risk Example)

Click **Welcome Week Sticker Pack** â†’ click **Product Snapshot**.

Slow down. Let the result land.

Say:

> "Here's the most important example. The sticker pack has the highest demand of all nine products â€” 80 units. But look at the score: At Risk."

Point to the margin.

Say:

> "The selling price is only 20 cents above cost. Students buy it constantly, but each sale barely earns anything. This is exactly why ProfitPilot exists."

---

## 1:25â€“1:55 â€” Test Scenario (Fix Before Applying)

Keep **Welcome Week Sticker Pack** selected. Click **Test Scenario**.

Enter:
- New Selling Price: `4.00`
- New Quantity: `80`

Click **Test Scenario**.

Say:

> "Instead of guessing, I can test a fix first. Raise the price to $4, keep the same demand â€” and ProfitPilot shows me the new profit, score, and decision before I commit. The score jumps, the decision changes."

Click **Apply Tested Scenario**.

Say:

> "One click applies it. The table, dashboard, and score all update automatically."

---

## 1:55â€“2:15 â€” Business Summary

Click **Business Summary**.

Say:

> "The Business Summary gives the full picture: total revenue, total profit, average score, best and weakest products, and a ranked list with suggested actions. This helps me quickly see what to promote, what to improve, and what might be risky."

---

## 2:15â€“2:35 â€” Break-Even Plan

Click **Break-Even Plan**. Enter fixed cost `500`. Click **Calculate Break-Even**.

Say:

> "The break-even planner estimates how many total units I need to sell to cover fixed costs â€” ingredients, packaging, a stall fee. It works across the whole product mix, so if margins are too weak overall, it tells me break-even isn't possible with the current setup."

---

## 2:35â€“3:00 â€” Export and Close

Close the break-even window. Click **Export Business Report**.

Say:

> "Finally, one click exports a plain text report and a styled HTML report that opens automatically â€” ready to present, print, or save as PDF."

Pause. Look at the audience. Smile.

Strong close:

> "Because popular doesn't mean profitable â€” and with ProfitPilot, you don't have to guess which is which. Thanks!"

Done.

---

## If Someone Asks To Add a Product Live

Say:

> "Sure â€” give me a name, cost, selling price, and expected quantity."

If nobody suggests one:

| Field | Value |
|---|---|
| Product Name | Cookie |
| Cost Price | 1.20 |
| Selling Price | 3.50 |
| Expected Quantity | 25 |

Click **Add Product** â†’ select â†’ **Product Snapshot**.

Say:

> "Quantity here means expected demand â€” how many I think I can sell in a week or at an event."

---

## If a Tutor Asks About the Code

> "The project is split into separate modules. `logic.py` handles all the calculations: revenue, profit, margin, score, what-if analysis, break-even, and recursive ranking. `profitpilot.py` is the Tkinter GUI. `storage.py` handles JSON save and load. `validators.py` parses and validates user input. `reports.py` generates the text and HTML exports. `test_profitpilot.py` runs seven unit tests against the calculation logic, all separate from the GUI so they can be tested cleanly."

Key functions to mention if asked:

- `calculate_metrics()` â€” full pipeline: revenue, cost, profit, margin, score, decision, recommendation
- `calculate_score()` â€” weighted scoring: 40% profit, 40% margin, 20% demand
- `what_if_analysis()` â€” simulates changes on a deep copy, doesn't touch saved data
- `rank_products_recursive()` â€” inserts products in score order using recursion
- `business_break_even()` â€” weighted average contribution per unit across all products
- `export_business_reports()` â€” writes `.txt` and `.html`, HTML opens via `webbrowser.open_new_tab()`

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

| Section | Time | Length |
|---|---|---|
| Opening hook | 0:00â€“0:15 | 15s |
| Load demo + dashboard | 0:15â€“0:35 | 20s |
| Product Snapshot (Matcha) | 0:35â€“1:00 | 25s |
| Sticker Pack risk example | 1:00â€“1:25 | 25s |
| Test Scenario + Apply | 1:25â€“1:55 | 30s |
| Business Summary | 1:55â€“2:15 | 20s |
| Break-Even Plan | 2:15â€“2:35 | 20s |
| Export + Close | 2:35â€“3:00 | 25s |
| **Total** | | **3:00** |

---

## What Changed From v2 (And Why)

**Tightened opening.** Cut "I'll show you how it works in under three minutes" â€” the demo speaks for itself.

**Merged narration in dashboard and Test Scenario sections.** Removed redundant lines like "Now I can make a confident decision" â€” the audience already sees the score jump.

**Fixed the awkward recursive-function line.** The old "It's a small detail, but it shows the logic is built properly, not just patched together" sounded defensive, like you were justifying the work. v3 just states the fact confidently and moves on. The deeper technical detail lives in the tutor Q&A section where it belongs.

**Rewrote the closing.** The old "small hustle" line trailed off. The new close calls back to the opening hook ("popular doesn't mean profitable") which is the line you want stuck in voters' heads when they pick. Cleanest way to win a vote: end on the same idea you opened with.

**Total time saved:** ~30 seconds across the script. You should now land comfortably at 3:00 (or slightly under) at your natural pace.
