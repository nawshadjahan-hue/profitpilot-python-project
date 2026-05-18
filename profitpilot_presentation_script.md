# ProfitPilot 3-Minute Presentation Script

## Before You Start

Open `Final Code/profitpilot.py` and run it.

Make sure the app window is visible and ready. If old saved products appear, you can still click `Load Campus Demo` during the presentation.

## 0:00-0:20 Opening

Smile.

Say:

"Hi everyone, my project is ProfitPilot, a campus business simulator. Imagine I am running a small USYD side hustle selling matcha, bubble tea, snacks, merch, and promo items. I designed it around students, but the same idea could also help small business owners compare products and make pricing decisions."

## 0:20-0:40 Dashboard

Point to the dashboard cards at the top.

Say:

"The top dashboard gives a quick business overview: how many products I have, total revenue, total profit, and the current top product."

Point to the score guide.

Say:

"The score is not random. It combines profit, margin, and demand, so it compares business performance instead of only showing sales."

## 0:40-1:00 Load Demo

Click `Load Campus Demo`.

Say:

"For the presentation, I will load sample campus products so we do not spend time typing everything manually. These are not the only products the app can use; users can add their own products on the left."

Point briefly to the left form.

Say:

"For a new product idea, the quantity can be used as expected demand, such as how many units I think I could sell in a week or during an event."

## 1:00-1:30 Product Snapshot

Select `Iced Matcha Latte`.

Click `Product Snapshot`.

Say:

"For one product, ProfitPilot calculates revenue, total cost, profit, margin, score, and a decision. Here it recommends whether this product is high potential, good, needs improvement, or risky."

Point to the recommendation text.

Say:

"This helps a beginner business owner understand the numbers, not just enter them."

## 1:30-1:55 Risk Example

Select `Welcome Week Sticker Pack`.

Click `Product Snapshot`.

Say:

"I also included a risky example. The sticker pack has high demand, but its selling price is very close to its cost, so the margin is weak. This shows that popular does not always mean profitable."

This is a good moment to show the app is not only positive; it can detect bad decisions too.

## 1:55-2:20 Test A Fix Before Applying

With `Welcome Week Sticker Pack` still selected, click `Test Scenario`.

Change:

- New Selling Price: `4.00`
- New Quantity: `80`

Click `Test Scenario`.

Say:

"Now I can test a real business strategy before changing my saved data. I increased the price to improve the margin, while keeping the same expected demand."

Point to the scenario result.

Say:

"ProfitPilot shows the new profit, margin, score, decision, and scenario tip first. This is safer than editing immediately, because I can check whether the change is actually a good idea."

Click `Apply Tested Scenario`.

Say:

"After reviewing the result, I can apply the tested scenario. ProfitPilot recalculates the product table, dashboard, and decision automatically."

Close the scenario window if it is still open, then click `Product Snapshot` again if you want to show the improved result.

## 2:20-2:35 Business Summary

Click `Business Summary`.

Say:

"The Business Summary gives the overall view. It shows total revenue, total profit, average score, best product, weakest product, and a ranking with suggested actions."

If asked about advanced concepts, you can mention that the product ranking is built using a recursive helper function.

## 2:35-2:50 Unrealistic Scenario Warning

Select `Bubble Tea` or `Iced Matcha Latte`.

Click `Test Scenario`.

Enter a small change, for example:

- New Selling Price: `8.50`
- New Quantity: `40`

Click `Test Scenario`.

Say:

"The Scenario Planner can also be used for another product. It lets me test a price or demand change without changing the saved product."

Point to the scenario result.

Say:

"It also warns if a price is technically profitable but unrealistic, because a very high selling price may not be achievable with real customers."

Optional warning demo:

- Change the tested selling price to a very high number, such as `600`.
- Click `Test Scenario`.
- Click `Apply Tested Scenario`.
- When the warning appears, click `No`.

Say:

"Even if the profit number looks high, ProfitPilot asks before applying a scenario that looks unrealistic."

## 2:50-2:57 Break-Even Plan

Close the scenario window.

Click `Break-Even Plan`.

Enter a fixed cost such as `500`.

Click `Calculate Break-Even`.

Say:

"The break-even planner estimates how many total sales are needed to cover fixed costs, such as ingredients, stall setup, packaging, or printing. It uses the whole product mix, so if the products do not have enough contribution per unit, it tells me break-even is not possible with the current mix."

## 2:57-3:00 Export And Close

Close the break-even window.

Click `Export Business Report`.

Say:

"Finally, the app exports a text report and a styled HTML business report. The HTML report opens automatically in the browser, so I can present it, print it, or save it as PDF."

End with:

"My goal was to turn simple product data into business decisions that a student seller could actually understand."

## If Someone Asks To Add A Product

Say:

"Sure, give me a product name, cost, selling price, and expected demand."

Use this quick example if nobody suggests one:

- Product Name: `Cookie`
- Cost Price: `1.20`
- Selling Price: `3.50`
- Expected Quantity: `25`

Say:

"Here, quantity is my estimated demand for the period I am testing."

Click `Add Product`, select it, then click `Product Snapshot`.

## Code Briefing For Tutor Questions

Main files:

- `profitpilot.py`: main Tkinter app, button callbacks, dashboard updates, and popups
- `logic.py`: revenue, profit, margin, score, recommendations, what-if analysis, break-even, and recursive ranking
- `storage.py`: JSON save/load file handling
- `validators.py`: input parsing and validation helpers
- `reports.py`: plain text and HTML report export
- `demo_data.py`: sample campus side-hustle products for the demo
- `test_profitpilot.py`: unit tests for the calculation logic
- `products.json`: saved product data
- `profitpilot_report.txt`: plain text report
- `profitpilot_report.html`: styled report that opens in the browser and can be saved as PDF

Important logic:

- `calculate_metrics()` calculates revenue, cost, profit, margin, score, decision, and recommendation.
- `calculate_score()` creates a score out of 100 using 40% profit, 40% margin, and 20% demand.
- `get_recommendation()` turns metrics into business advice.
- `what_if_analysis()` simulates price and quantity changes without changing original saved data.
- `apply_scenario_to_product()` applies a tested scenario only after the user has reviewed the result.
- `business_break_even()` estimates break-even units for the whole product mix.
- `rank_products_recursive()` ranks products by score using recursion.
- `save_products()` and `load_products()` use JSON file input/output.
- `export_business_report()` creates the text and HTML reports.
- `webbrowser.open_new_tab()` opens the HTML report automatically after export.
- `build_gui()` creates the Tkinter interface.

Editing workflow:

- `start_edit_selected()` loads the selected product into the left form.
- The same `add_product()` function handles both adding and editing.
- `edit_mode_index` stores whether the form is currently editing an existing product.
- After saving an edit, `recalculate_all_metrics()` updates the score, decision, dashboard, and product table.

Advanced topics shown:

- File I/O with JSON and report export
- Exception handling for invalid input and damaged files
- Recursion for product ranking in the business summary
- GUI programming with Tkinter
- Testing with `unittest`

## Unit Test Briefing

Say:

"I separated the calculation logic from the GUI, so I can test the business calculations without opening the app."

The tests check:

- `test_calculate_metrics_adds_business_values`: revenue, cost, profit, margin, score, decision, and recommendation are created correctly.
- `test_break_even_units_returns_required_units`: break-even formula works when contribution per unit is positive.
- `test_break_even_units_returns_none_when_no_contribution`: break-even returns `None` if the product cannot cover costs.
- `test_what_if_analysis_does_not_change_original_product`: scenario testing does not overwrite saved product data.
- `test_business_break_even_uses_all_products`: business-level break-even uses the whole product mix.
- `test_loss_making_product_is_at_risk`: a product selling below cost is marked as risky.
- `test_score_breakdown_matches_total_score`: the score explanation matches the final score.

Command:

```bash
python -m unittest test_profitpilot.py
```

Expected result:

```text
Ran 7 tests
OK
```
