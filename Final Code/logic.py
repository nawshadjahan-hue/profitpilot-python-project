"""Business calculations and decision helpers for ProfitPilot.

This module contains pure Python logic only. It does not create Tkinter
widgets or show message boxes, so these functions can be tested separately
from the graphical interface.
"""

import math


def calculate_score(product: dict, products: list) -> int:
    """
    Calculate a product score out of 100.

    Suggested weighting:
    - Profit score: 40
    - Margin score: 40
    - Quantity score: 20
    """
    # -------------------------
    # A) Profit score (out of 40)
    # -------------------------
    # Recompute profits from raw values
    positive_profits = []
    for item in products:
        try:
            cost = float(item.get("cost", 0))
            price = float(item.get("price", 0))
            quantity = float(item.get("quantity", 0))
        except (TypeError, ValueError):
            continue

        item_profit = (price * quantity) - (cost * quantity)
        if item_profit > 0:
            positive_profits.append(item_profit)

    # Current product profit: use existing value if available, otherwise recompute.
    try:
        current_profit = float(product.get("profit", (float(product.get("price", 0)) * float(product.get("quantity", 0))) - (float(product.get("cost", 0)) * float(product.get("quantity", 0)))))
    except (TypeError, ValueError):
        current_profit = 0.0

    if not positive_profits:
        profit_score = 0.0
    else:
        max_profit = max(positive_profits)
        profit_score = (max(current_profit, 0.0) / max_profit) * 40.0

    # -------------------------
    # B) Margin score (out of 40)
    # -------------------------
    try:
        margin = float(product.get("margin", 0))
    except (TypeError, ValueError):
        margin = 0.0

    if margin <= 0:
        margin_score = 0.0
    elif margin >= 40:
        margin_score = 40.0
    else:
        margin_score = (margin / 40.0) * 40.0

    # -------------------------
    # C) Quantity score (out of 20)
    # -------------------------
    quantities = []
    for item in products:
        try:
            quantities.append(float(item.get("quantity", 0)))
        except (TypeError, ValueError):
            continue

    max_quantity = max(quantities) if quantities else 0.0

    try:
        product_quantity = float(product.get("quantity", 0))
    except (TypeError, ValueError):
        product_quantity = 0.0

    if max_quantity <= 0:
        quantity_score = 0.0
    else:
        quantity_score = (max(product_quantity, 0.0) / max_quantity) * 20.0

    # -------------------------
    # D) Final score (0 to 100)
    # -------------------------
    score = round(profit_score + margin_score + quantity_score)
    score = max(0, min(100, int(score)))
    return score


def calculate_score_breakdown(product: dict, products: list) -> dict:
    """
    Calculate the score components used in the ProfitPilot score.
    Returns profit, margin, demand, and total score values.
    """
    positive_profits = []
    for item in products:
        try:
            cost = float(item.get("cost", 0))
            price = float(item.get("price", 0))
            quantity = float(item.get("quantity", 0))
        except (TypeError, ValueError):
            continue

        item_profit = (price * quantity) - (cost * quantity)
        if item_profit > 0:
            positive_profits.append(item_profit)

    try:
        current_profit = float(product.get("profit", 0))
    except (TypeError, ValueError):
        current_profit = 0.0

    max_profit = max(positive_profits) if positive_profits else 0.0
    if max_profit > 0:
        profit_component = (max(current_profit, 0.0) / max_profit) * 40.0
    else:
        profit_component = 0.0

    try:
        margin = float(product.get("margin", 0))
    except (TypeError, ValueError):
        margin = 0.0

    if margin <= 0:
        margin_component = 0.0
    elif margin >= 40:
        margin_component = 40.0
    else:
        margin_component = margin

    quantities = []
    for item in products:
        try:
            quantities.append(float(item.get("quantity", 0)))
        except (TypeError, ValueError):
            continue

    max_quantity = max(quantities) if quantities else 0.0
    try:
        product_quantity = float(product.get("quantity", 0))
    except (TypeError, ValueError):
        product_quantity = 0.0

    if max_quantity <= 0:
        demand_component = 0.0
    else:
        demand_component = (max(product_quantity, 0.0) / max_quantity) * 20.0

    total = round(profit_component + margin_component + demand_component)
    total = max(0, min(100, int(total)))

    return {
        "profit": profit_component,
        "margin": margin_component,
        "demand": demand_component,
        "total": total,
        "product_profit": current_profit,
        "max_profit": max_profit,
        "product_margin": margin,
        "product_quantity": product_quantity,
        "max_quantity": max_quantity
    }


def get_status(score: int) -> str:
    """
    Convert numeric score into a performance label.
    """
    if score >= 80:
        return "High Potential"
    elif score >= 60:
        return "Good Performer"
    elif score >= 40:
        return "Needs Improvement"
    else:
        return "At Risk"


def get_recommendation(product: dict) -> str:
    """
    Return a recommendation string based on product metrics.
    Expects product to already contain:
    - profit
    - margin
    - score
    """
    try:
        profit = float(product.get("profit", 0))
    except (TypeError, ValueError):
        profit = 0.0

    try:
        margin = float(product.get("margin", 0))
    except (TypeError, ValueError):
        margin = 0.0

    try:
        score = int(product.get("score", 0))
    except (TypeError, ValueError):
        score = 0

    try:
        quantity = int(product.get("quantity", 0))
    except (TypeError, ValueError):
        quantity = 0

    if profit < 0:
        return "Business Doctor says: this product is losing money. Increase price, reduce cost, or stop selling it."
    elif quantity >= 35 and margin < 20:
        return "Popular but not powerful. Students buy it often, but each sale earns too little profit."
    elif margin < 10:
        return "Low margin warning. The product sells, but the business keeps only a small part of the revenue."
    elif score >= 80:
        return "Star product. Promote this more because it has strong profit, margin, and demand."
    elif score >= 60:
        return "Good performer. Keep selling it, but monitor price and costs."
    else:
        return "Needs improvement. Try changing the price, reducing cost, or selling it in a bundle."


def get_scenario_recommendation(original_product: dict, scenario_product: dict) -> str:
    """
    Return recommendation text specifically for what-if scenarios.
    Compares original performance with simulated performance.
    """
    try:
        original_profit = float(original_product.get("profit", 0))
    except (TypeError, ValueError):
        original_profit = 0.0

    try:
        original_score = float(original_product.get("score", 0))
    except (TypeError, ValueError):
        original_score = 0.0

    try:
        new_profit = float(scenario_product.get("profit", 0))
    except (TypeError, ValueError):
        new_profit = 0.0

    try:
        new_score = float(scenario_product.get("score", 0))
    except (TypeError, ValueError):
        new_score = 0.0

    try:
        original_price = float(original_product.get("price", 0))
    except (TypeError, ValueError):
        original_price = 0.0

    try:
        new_price = float(scenario_product.get("price", 0))
    except (TypeError, ValueError):
        new_price = 0.0

    try:
        new_margin = float(scenario_product.get("margin", 0))
    except (TypeError, ValueError):
        new_margin = 0.0

    if new_profit < 0:
        message = "This scenario is not sustainable because it leads to a loss."

    elif new_score > original_score + 10:
        if new_score >= 60:
            message = "This scenario significantly improves performance. Consider testing this strategy."
        else:
            message = "This scenario improves performance, but the product still remains At Risk."

    elif new_score > original_score:
        message = "This scenario provides a small improvement."

    elif new_score == original_score:
        message = "This scenario makes little difference."

    else:
        message = "This scenario reduces performance."

    if new_price > original_price and new_profit > original_profit:
        message += " Increasing price improves profitability in this scenario."

    if original_price > 0 and new_price >= original_price * 2:
        message += " Feasibility warning: this price is much higher than the current price, so check whether customers would realistically still buy it."
    elif new_margin >= 80:
        message += " Feasibility warning: the margin is extremely high, so the price may be unrealistic for customers."

    return message


def calculate_metrics(product: dict, products: list) -> dict:
    """
    Calculate and attach metrics to a product dictionary.

    Expected input keys:
    - name
    - cost
    - price
    - quantity

    Adds:
    - revenue
    - total_cost
    - profit
    - margin
    - score
    - status
    - recommendation
    """
    # Read raw values safely.
    # Inputs are already validated, but this keeps the function robust.
    try:
        cost = float(product.get("cost", 0))
    except (TypeError, ValueError):
        cost = 0.0

    try:
        price = float(product.get("price", 0))
    except (TypeError, ValueError):
        price = 0.0

    try:
        quantity = int(product.get("quantity", 0))
    except (TypeError, ValueError):
        quantity = 0

    # Core metrics
    revenue = price * quantity
    total_cost = cost * quantity
    profit = revenue - total_cost

    if revenue > 0:
        margin = (profit / revenue) * 100.0
    else:
        # Avoid division by zero.
        margin = 0.0

    # Store temporary metrics before scoring/recommendation.
    product["revenue"] = revenue
    product["total_cost"] = total_cost
    product["profit"] = profit
    product["margin"] = margin

    # Score/status/recommendation pipeline
    score = calculate_score(product, products)
    status = get_status(score)
    product["score"] = score
    product["status"] = status
    product["recommendation"] = get_recommendation(product)

    return product


def break_even_units(product: dict, fixed_cost: float):
    """
    Calculate break-even units for the given product.

    Formula:
    contribution per unit = price - cost
    break-even units = fixed_cost / contribution per unit
    """
    try:
        price = float(product.get("price", 0))
    except (TypeError, ValueError):
        price = 0.0

    try:
        cost = float(product.get("cost", 0))
    except (TypeError, ValueError):
        cost = 0.0

    contribution = price - cost

    # Break-even impossible if contribution per unit is zero or negative.
    if contribution <= 0:
        return None

    # fixed_cost is validated in caller, but guard here too.
    if fixed_cost < 0:
        return None

    break_even = fixed_cost / contribution
    return math.ceil(break_even)


def what_if_analysis(product: dict, products: list, new_price: float, new_quantity: int) -> dict:
    """
    Perform temporary analysis without permanently changing saved product data.
    Returns a new dictionary with recalculated values using a temporary product list.
    """
    if new_price < 0 or new_quantity < 0:
        raise ValueError("Price and quantity must be non-negative.")

    # Temporary copy of selected product
    temp_product = dict(product)
    temp_product["price"] = float(new_price)
    temp_product["quantity"] = int(new_quantity)

    # Temporary product list copy
    temp_products = [dict(item) for item in products]

    # Find and replace selected product in temporary product list
    selected_index = None
    for i, item in enumerate(products):
        if item is product:
            selected_index = i
            break

    # Fallback matching for safety (if identity match fails)
    if selected_index is None:
        for i, item in enumerate(products):
            if (
                item.get("name") == product.get("name")
                and item.get("cost") == product.get("cost")
                and item.get("price") == product.get("price")
                and item.get("quantity") == product.get("quantity")
            ):
                selected_index = i
                break

    if selected_index is not None:
        temp_products[selected_index] = temp_product
    else:
        temp_products.append(temp_product)

    # Compute metrics/score/status/recommendation against the temporary product list
    analyzed_product = calculate_metrics(temp_product, temp_products)
    scenario_recommendation = get_scenario_recommendation(product, analyzed_product)
    analyzed_product["scenario_recommendation"] = scenario_recommendation
    return analyzed_product


def make_score_bar(score: int) -> str:
    """
    Create a simple visual rating for the ProfitPilot score.
    """
    if score >= 80:
        return "Rating           : Excellent product to promote"
    elif score >= 60:
        return "Rating           : Solid product to keep selling"
    elif score >= 40:
        return "Rating           : Needs a pricing or cost review"
    else:
        return "Rating           : High risk for the business"


def get_business_action(status: str) -> str:
    """
    Convert a decision label into a short business action.
    """
    if status == "High Potential":
        return "Promote"
    elif status == "Good Performer":
        return "Keep selling"
    elif status == "Needs Improvement":
        return "Review"
    else:
        return "High risk"


def business_break_even(products_list: list, fixed_cost: float):
    """
    Calculate business-level break-even units using all products together.
    """
    if fixed_cost < 0 or not products_list:
        return None

    total_units = sum(float(item.get("quantity", 0)) for item in products_list)
    if total_units <= 0:
        return None

    total_contribution = 0.0
    for item in products_list:
        try:
            price = float(item.get("price", 0))
            cost = float(item.get("cost", 0))
            quantity = float(item.get("quantity", 0))
        except (TypeError, ValueError):
            continue
        total_contribution += (price - cost) * quantity

    if total_contribution <= 0:
        return None

    avg_contribution_per_unit = total_contribution / total_units
    if avg_contribution_per_unit <= 0:
        return None

    return math.ceil(fixed_cost / avg_contribution_per_unit)


def recalculate_all_products(products: list) -> list:
    """
    Recalculate metrics for every product and return a new updated list.

    This keeps business calculations independent from the Tkinter interface,
    which makes the logic easier to test and reuse.
    """
    updated_products = [dict(product) for product in products]
    for index, product in enumerate(updated_products):
        updated_products[index] = calculate_metrics(product, updated_products)
    return updated_products


def rank_products_recursive(products: list, index: int = 0, ranked_products: list | None = None) -> list:
    """
    Recursively build a product ranking from highest score to lowest score.

    Advanced topic: recursion. The base case happens when every product has
    been visited. Each recursive call processes one product and inserts it into
    the ranked list in score order.
    """
    if ranked_products is None:
        ranked_products = []

    if index >= len(products):
        return ranked_products

    current_product = products[index]
    current_score = int(current_product.get("score", 0))
    insert_position = 0

    while insert_position < len(ranked_products):
        existing_score = int(ranked_products[insert_position].get("score", 0))
        if current_score > existing_score:
            break
        insert_position += 1

    ranked_products.insert(insert_position, current_product)
    return rank_products_recursive(products, index + 1, ranked_products)

