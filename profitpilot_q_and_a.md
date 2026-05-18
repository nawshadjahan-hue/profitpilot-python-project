# ProfitPilot Q&A Practice

Use this file to collect likely tutor/classmate questions and short answers.

## What is ProfitPilot?

ProfitPilot is a campus side-hustle business simulator. It helps users compare products, understand profit and margin, test price changes, estimate break-even sales, and export a business report.

## Is this just a profit calculator?

No. A calculator only gives numbers. ProfitPilot turns product data into business decisions, such as what to promote, what to keep selling, what to review, and what may be risky.

## What does the ProfitPilot score mean?

The score is a simple decision score out of 100. It combines:

- Profit: 40%
- Margin: 40%
- Demand: 20%

The goal is to avoid choosing a product only because it sells many units. A strong product should have a good balance of total profit, profit per sale, and customer demand.

## Why did you choose 40% profit, 40% margin, and 20% demand?

Profit and margin are weighted most strongly because a business needs to make money overall and keep enough profit from each sale. Demand is still included, but it has a smaller weight because high sales are not helpful if each sale earns very little.

## Could the score weights change for different businesses?

Yes. In this version, the weights are fixed to keep the logic clear and explainable. A future version could let users customise the weights. For example, a new startup might care more about demand, while a small seller with limited stock might care more about margin.

## Could the score use past data?

Yes. A future version could save weekly or monthly records and use past performance to show trends. For example, it could compare whether bubble tea sales are increasing week by week or whether a product's margin is getting worse over time.

## Is the app analysing one day, one week, or one month?

The app analyses one business period at a time. The user can decide what the period means:

- one day
- one week
- one month
- one campus event

The quantity field can mean actual sales for a past period or expected demand for a planned period.

## Why not use a product with selling price below cost?

Selling below cost can happen in discounts or promotions, but it may feel unrealistic for a normal product. That is why the demo uses a better business example: the Welcome Week Sticker Pack has high demand but the price is too close to the cost. It sells many units, but the margin is weak, so ProfitPilot marks it as risky.

## If one product has the highest profit but another product has better margin, which should be the top product?

It depends on the business goal. ProfitPilot does not choose based on profit alone. It uses the combined score:

- high profit helps
- high margin helps
- strong demand helps

So a product with slightly lower total profit but much better margin and demand could become the top product. This is intentional because a business decision should consider both total money earned and how efficiently the product earns it.

## Why might a popular product be risky?

A product can sell many units but still be weak if the selling price is too close to the cost. In that case, the business is doing a lot of work for very little profit per sale.

## What margin should a business target?

In this project, 40% margin is treated as a strong target. A product gets full margin score when it reaches 40% or more.

As a simple guide:

- 40% or higher: strong
- 20% to 40%: reasonable, but can be improved
- 10% to 20%: weak
- below 10%: risky unless demand is extremely strong

The exact target can vary by business type. Food, merch, handmade items, and digital products may all have different normal margins.

## Why should users test a scenario before applying it?

Changing the actual product price immediately can be risky. The Scenario Planner lets the user test a new price and expected demand first. If the result looks realistic, the user can then choose Apply Tested Scenario to update the product.

## What happens if a scenario uses an unrealistic price?

The app now warns the user when the tested selling price is much higher than the current price or when the margin becomes extremely high. This is important because a price can look profitable in calculation but still fail if customers would not realistically pay it.

## What does break-even mean in this app?

Break-even means the estimated number of total units needed to cover fixed costs. Fixed costs could include stall setup, printing, packaging, equipment, or event fees.

The app uses the whole product mix. It estimates average contribution per unit across all products and compares that with the fixed cost.

## When is break-even not possible?

Break-even is not possible when the current product mix has no positive contribution. For example, if products are priced too close to cost or below cost, selling more units may not cover fixed costs effectively.

## How would a real side-hustle owner use this from day 1 to day N?

Day 1: enter products and estimated demand.

During the week: update price, cost, or quantity using Edit Selected.

End of week: click Business Summary and export the report.

Next week/month: update the product values for the new period and export another report.

This version works as a period-based business snapshot. A future version could store multiple dated reports and compare trends over time.

## Why use Tkinter instead of a web app?

Tkinter is included with standard Python, so the tutor can run the project without installing extra libraries. A future version could be built as a Flask or Streamlit web app, but for this assessment the desktop app is safer and easier to submit.

## What advanced topics does the project show?

The project shows:

- File I/O with JSON save/load and report export
- Exception handling for invalid input and damaged files
- Recursion for ranking products in the business summary
- GUI programming with Tkinter
- Testing with Python unittest

## Why did you split the code into multiple files?

I split the project so each file has one clear job. `profitpilot.py` controls the Tkinter interface, `logic.py` contains the business calculations, `storage.py` handles JSON files, `validators.py` checks user input, `reports.py` exports reports, and `demo_data.py` stores the sample products. This makes the program easier to read, test, and maintain.

## How did you test the project?

I created `test_profitpilot.py` using Python's unittest module. It imports `logic.py` directly, so the calculation logic can be tested without opening the Tkinter window. It tests metric calculations, break-even calculation, what-if analysis, business break-even, score breakdown, and whether a loss-making product is marked as risky.
