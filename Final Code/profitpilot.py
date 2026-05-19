"""ProfitPilot graphical application.

This file contains the Tkinter interface and user-event callbacks. Business
calculations, validation, file storage, reports, and demo data are separated
into smaller modules so the project is easier to read, test, and maintain.
"""

import os
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

from demo_data import get_campus_demo_products
from logic import (
    business_break_even,
    calculate_metrics,
    calculate_score_breakdown,
    get_business_action,
    make_score_bar,
    rank_products_recursive,
    recalculate_all_products,
    what_if_analysis,
)
from reports import export_business_reports
from storage import load_products_from_file, save_products_to_file
from validators import safe_parse_float, safe_parse_int

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "products.json")
products = []

# Global widget references
root = None
name_entry = None
cost_entry = None
price_entry = None
qty_entry = None
feedback_label = None
product_tree = None
analysis_text = None
status_label = None
dashboard_value_labels = {}
product_form_title = None
submit_product_button = None
edit_mode_index = None


def save_products():
    """Save product data using the storage module and report the result in the GUI."""
    try:
        save_products_to_file(products, DATA_FILE)
        if feedback_label is not None:
            feedback_label.config(text="Data saved successfully.")
        messagebox.showinfo("Save Data", "Products saved successfully.")
    except (OSError, TypeError, ValueError):
        messagebox.showerror("Save Error", "Data could not be saved. Please try again.")


def load_products(show_message: bool = True):
    """Load saved product data using the storage module."""
    global products

    try:
        products = load_products_from_file(DATA_FILE)
    except FileNotFoundError:
        products = []
        refresh_product_tree()
        show_score_guide()
        update_status_label("")
        if feedback_label is not None:
            feedback_label.config(text="No saved products found yet.")
        if show_message:
            messagebox.showinfo("Load Data", "No saved products were found yet.")
        return
    except (OSError, TypeError, ValueError):
        if feedback_label is not None:
            feedback_label.config(text="Saved data could not be loaded.")
        if show_message:
            messagebox.showerror(
                "Load Error",
                "Saved data could not be loaded. The file may be damaged or in an invalid format."
            )
        return

    recalculate_all_metrics()
    refresh_product_tree()
    show_score_guide()
    update_status_label("")

    if feedback_label is not None:
        if products:
            feedback_label.config(text=f"Loaded {len(products)} saved products.")
        else:
            feedback_label.config(text="Saved file is empty. No products to show.")
            if show_message:
                messagebox.showinfo("Load Data", "The saved file is empty. No products were loaded.")






def clear_fields():
    """
    Clear all input fields and return the form to add mode.
    """
    global edit_mode_index

    if name_entry is not None:
        name_entry.delete(0, tk.END)
    if cost_entry is not None:
        cost_entry.delete(0, tk.END)
    if price_entry is not None:
        price_entry.delete(0, tk.END)
    if qty_entry is not None:
        qty_entry.delete(0, tk.END)

    edit_mode_index = None
    if product_form_title is not None:
        product_form_title.config(text="Add Product")
    if submit_product_button is not None:
        submit_product_button.config(text="Add Product")

    if feedback_label is not None:
        feedback_label.config(text="")


def validate_inputs():
    """
    Validate and parse user inputs.

    Returns:
        tuple: (name, cost, price, quantity)

    Raises:
        ValueError if input is invalid.
    """
    if any(w is None for w in (name_entry, cost_entry, price_entry, qty_entry)):
        raise ValueError("Please complete all product fields before adding a product.")
    
    name = name_entry.get().strip()
    cost_text = cost_entry.get().strip()
    price_text = price_entry.get().strip()
    qty_text = qty_entry.get().strip()

    if not name:
        raise ValueError("Please enter a product name.")

    cost = safe_parse_float(
        cost_text,
        "Please enter a cost price.",
        "Please enter a valid number for cost price."
    )
    price = safe_parse_float(
        price_text,
        "Please enter a selling price.",
        "Please enter a valid number for selling price."
    )
    quantity = safe_parse_int(
        qty_text,
        "Please enter an expected quantity.",
        "Please enter a valid whole number for expected quantity."
    )

    if cost < 0 or price < 0 or quantity < 0:
        raise ValueError("Cost, price, and quantity cannot be negative.")

    return name, cost, price, quantity


def confirm_risky_product_change(original_product: dict, updated_product: dict, parent=None) -> bool:
    """
    Ask before applying a change that lowers performance or looks unrealistic.
    """
    current_score = int(original_product.get("score", 0))
    tested_score = int(updated_product.get("score", 0))
    current_profit = float(original_product.get("profit", 0))
    tested_profit = float(updated_product.get("profit", 0))
    current_price = float(original_product.get("price", 0))
    tested_price = float(updated_product.get("price", 0))
    tested_margin = float(updated_product.get("margin", 0))

    if tested_score < current_score or tested_profit < current_profit:
        apply_anyway = messagebox.askyesno(
            "Lower Performance Warning",
            (
                "This change may lower performance.\n\n"
                f"Current Score: {current_score}/100\n"
                f"New Score: {tested_score}/100\n"
                f"Current Profit: ${current_profit:.2f}\n"
                f"New Profit: ${tested_profit:.2f}\n\n"
                "Do you still want to apply it?"
            ),
            parent=parent
        )
        if not apply_anyway:
            return False

    if (current_price > 0 and tested_price >= current_price * 2) or tested_margin >= 80:
        apply_anyway = messagebox.askyesno(
            "Feasibility Warning",
            (
                "This change may be unrealistic for real customers.\n\n"
                f"Current Price: ${current_price:.2f}\n"
                f"New Price: ${tested_price:.2f}\n"
                f"New Margin: {tested_margin:.2f}%\n\n"
                "Do you still want to apply it?"
            ),
            parent=parent
        )
        if not apply_anyway:
            return False

    return True


def add_product():
    """
    Read inputs, validate, and add or update a product.
    """
    global edit_mode_index

    try:
        name, cost, price, quantity = validate_inputs()

        product = {
            "name": name,
            "cost": cost,
            "price": price,
            "quantity": quantity
        }

        if edit_mode_index is None:
            products.append(product)
            feedback_message = f"Added product: {name}"
        else:
            draft_products = [dict(item) for item in products]
            draft_products[edit_mode_index] = dict(product)
            updated_product = calculate_metrics(dict(product), draft_products)
            if not confirm_risky_product_change(products[edit_mode_index], updated_product, root):
                return

            products[edit_mode_index] = product
            feedback_message = f"Updated product: {name}"

        recalculate_all_metrics()
        refresh_product_tree()
        if edit_mode_index is not None and product_tree is not None:
            product_tree.selection_set(str(edit_mode_index))
            product_tree.focus(str(edit_mode_index))
        clear_fields()

        if feedback_label is not None:
            feedback_label.config(text=feedback_message)

    except ValueError as error:
        if feedback_label is not None:
            feedback_label.config(text=str(error))
        title = "Missing Input" if "Please enter" in str(error) else "Invalid Input"
        messagebox.showwarning(title, str(error))


def start_edit_selected():
    """
    Load the selected product into the left form for editing.
    """
    global edit_mode_index

    selected_index = get_selected_product_index()
    if selected_index is None:
        return

    product = products[selected_index]
    edit_mode_index = selected_index

    clear_entry_widgets_only()

    name_entry.insert(0, str(product.get("name", "")))
    cost_entry.insert(0, str(product.get("cost", "")))
    price_entry.insert(0, str(product.get("price", "")))
    qty_entry.insert(0, str(product.get("quantity", "")))

    if product_form_title is not None:
        product_form_title.config(text="Edit Product")
    if submit_product_button is not None:
        submit_product_button.config(text="Save Changes")
    if feedback_label is not None:
        feedback_label.config(text="Editing selected product. Save changes or clear fields to cancel.")


def clear_entry_widgets_only():
    """
    Clear input widgets without changing add/edit mode.
    """
    if name_entry is not None:
        name_entry.delete(0, tk.END)
    if cost_entry is not None:
        cost_entry.delete(0, tk.END)
    if price_entry is not None:
        price_entry.delete(0, tk.END)
    if qty_entry is not None:
        qty_entry.delete(0, tk.END)


def refresh_product_tree():
    """
    Refresh Treeview with current products list.
    """
    if product_tree is None:
        return

    # Clear existing rows
    for item in product_tree.get_children():
        product_tree.delete(item)

    # Insert current products
    for index, product in enumerate(products):
        product_tree.insert(
            "",
            "end",
            iid=str(index),
            values=(
                product.get("name", ""),
                product.get("cost", 0),
                product.get("price", 0),
                product.get("quantity", 0),
                f"${float(product.get('profit', 0)):.2f}",
                f"{int(product.get('score', 0))}/100",
                product.get("status", "")
            )
        )

    update_dashboard_summary()


def update_dashboard_summary():
    """
    Update the main dashboard cards using the current product list.
    """
    if not dashboard_value_labels:
        return

    if not products:
        summary_values = {
            "products": "0",
            "revenue": "$0.00",
            "profit": "$0.00",
            "top": "No products yet"
        }
    else:
        total_revenue = sum(float(product.get("revenue", 0)) for product in products)
        total_profit = sum(float(product.get("profit", 0)) for product in products)
        best_product = max(products, key=lambda p: int(p.get("score", 0)))
        summary_values = {
            "products": str(len(products)),
            "revenue": f"${total_revenue:.2f}",
            "profit": f"${total_profit:.2f}",
            "top": str(best_product.get("name", "Unknown"))
        }

    for key, value in summary_values.items():
        label = dashboard_value_labels.get(key)
        if label is not None:
            label.config(text=value)


def get_selected_product_index():
    """
    Return selected product index from Treeview.
    """
    if product_tree is None:
        return None

    selected_items = product_tree.selection()
    if not selected_items:
        messagebox.showwarning("No Selection", "Please select a product first.")
        return None

    return int(selected_items[0])


def show_analysis_text(text: str):
    """
    Display text inside the analysis panel.
    """
    if analysis_text is None:
        return

    analysis_text.config(state="normal")
    analysis_text.delete("1.0", tk.END)

    analysis_text.tag_configure("title", font=("Segoe UI", 12, "bold"))
    analysis_text.tag_configure("section", font=("Segoe UI", 11, "bold"))
    analysis_text.tag_configure("hint", foreground="#444444", font=("Segoe UI", 10))
    analysis_text.tag_configure("normal", font=("Consolas", 10))

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            analysis_text.insert(tk.END, "\n")
        elif stripped.startswith(("PRODUCT ANALYSIS", "BUSINESS SUMMARY", "BUSINESS DECISION GUIDE")):
            analysis_text.insert(tk.END, f"{line}\n", "title")
        elif stripped.startswith(("Recommendation", "What these mean:", "Score Calculation", "Summary Help:", "Product Ranking", "Score Guide", "Score Mix", "Business Tip")):
            analysis_text.insert(tk.END, f"{line}\n", "section")
        elif stripped.startswith("- "):
            analysis_text.insert(tk.END, f"{line}\n", "hint")
        else:
            analysis_text.insert(tk.END, f"{line}\n", "normal")

    analysis_text.config(state="disabled")


def show_score_guide():
    """
    Show a plain-English guide before the user runs an analysis.
    """
    guide = (
        "BUSINESS DECISION GUIDE\n\n"
        "ProfitPilot helps you compare products before deciding what to promote, improve, or stop selling.\n\n"
        "Score Guide\n"
        "80-100 : Promote this product\n"
        "60-79  : Keep selling and monitor\n"
        "40-59  : Review price or cost\n"
        "0-39   : High business risk\n\n"
        "Score Mix\n"
        "Profit : 40%  money earned overall\n"
        "Margin : 40%  profit kept from each sale\n"
        "Demand : 20%  quantity customers buy\n\n"
        "Business Tip\n"
        "Popular does not always mean profitable. The best product balances demand with strong profit."
    )
    show_analysis_text(guide)
    update_status_label("Decision Guide")


def update_status_label(status: str):
    """
    Update the colored status label.
    """
    if status_label is None:
        return

    if not status:
        status_label.config(text="Decision:", fg="black")
        return

    if status == "High Potential":
        status_label.config(text="Decision: High Potential", fg="green")
    elif status == "Good Performer":
        status_label.config(text="Decision: Good Performer", fg="#1f5f8b")
    elif status == "Needs Improvement":
        status_label.config(text="Decision: Needs Improvement", fg="orange")
    elif status == "At Risk":
        status_label.config(text="Decision: At Risk", fg="red")
    elif status == "Overall Summary":
        status_label.config(text="View: Business Summary", fg="purple")
    elif status == "Decision Guide":
        status_label.config(text="View: Decision Guide", fg="purple")
    else:
        status_label.config(text=f"Decision: {status}", fg="black")






def analyze_selected():
    """
    Analyze the currently selected product and display detailed metrics.
    """
    selected_index = get_selected_product_index()
    if selected_index is None:
        return

    product = products[selected_index]
    product = calculate_metrics(product, products)
    products[selected_index] = product

    profit_value = product["profit"]
    profit_text = f"-${abs(profit_value):.2f}" if profit_value < 0 else f"${profit_value:.2f}"
    score_bar = make_score_bar(product["score"])
    score_breakdown = calculate_score_breakdown(product, products)

    output = (
        "PRODUCT ANALYSIS\n\n"
        f"Product           : {product['name']}\n\n"
        f"Revenue          : ${product['revenue']:.2f}\n"
        f"Total Cost       : ${product['total_cost']:.2f}\n"
        f"Profit           : {profit_text}\n"
        f"Margin           : {product['margin']:.2f}%\n"
        f"ProfitPilot Score: {product['score']}/100\n"
        f"{score_bar}\n"
        f"Decision         : {product['status']}\n\n"
        "Recommendation\n"
        f"{product['recommendation']}\n\n"
        "Score Calculation\n"
        "Profit strength  : product profit / highest profit x 40\n"
        f"                   ${score_breakdown['product_profit']:.2f} / ${score_breakdown['max_profit']:.2f} x 40 = {score_breakdown['profit']:.1f}/40\n"
        "Margin strength  : margin / 40% x 40, capped at 40\n"
        f"                   {score_breakdown['product_margin']:.2f}% gives {score_breakdown['margin']:.1f}/40\n"
        "Demand strength  : product quantity / highest quantity x 20\n"
        f"                   {score_breakdown['product_quantity']:.0f} / {score_breakdown['max_quantity']:.0f} x 20 = {score_breakdown['demand']:.1f}/20\n"
        f"Total score      : {score_breakdown['profit']:.1f} + {score_breakdown['margin']:.1f} + {score_breakdown['demand']:.1f} = {score_breakdown['total']}/100\n\n"
        "What these mean:\n"
        "- Margin = profit made per sale as a percentage.\n"
        "- Score = a quick combined view of profit, efficiency, and sales."
    )

    show_analysis_text(output)
    update_status_label(product["status"])


def analyze_all():
    """
    Analyze all products and show overall business summary.
    """
    if not products:
        messagebox.showwarning("No Products", "Please add at least one product first.")
        return

    # Recalculate all products first because scores compare products against the current list.
    recalculate_all_metrics()

    total_revenue = sum(product["revenue"] for product in products)
    total_profit = sum(product["profit"] for product in products)
    total_score = sum(product["score"] for product in products)
    average_score = total_score / len(products)

    best_product = max(products, key=lambda p: p["score"])
    worst_product = min(products, key=lambda p: p["score"])
    sorted_products = rank_products_recursive(products)
    product_rows = "\n".join(
        (
            f"{rank}. {product['name']}\n"
            f"   Profit   : ${product['profit']:.2f}\n"
            f"   Score    : {product['score']}/100\n"
            f"   Action   : {get_business_action(product['status'])}"
        )
        for rank, product in enumerate(sorted_products, start=1)
    )

    output = (
        "BUSINESS SUMMARY\n\n"
        f"Total Products   : {len(products)}\n"
        f"Total Revenue    : ${total_revenue:.2f}\n"
        f"Total Profit     : ${total_profit:.2f}\n"
        f"Average Score    : {average_score:.0f}/100\n\n"
        f"Best Product     : {best_product['name']} ({best_product['score']}/100)\n"
        f"Weakest Product  : {worst_product['name']} ({worst_product['score']}/100)\n\n"
        "Product Ranking\n"
        f"{product_rows}\n\n"
        "Summary Help:\n"
        "- Best Product = strongest product in your current product list.\n"
        "- Average Score = average performance across all entered products."
    )

    show_analysis_text(output)
    update_status_label("Overall Summary")


def delete_selected():
    """
    Delete selected product from list.
    """
    selected_index = get_selected_product_index()
    if selected_index is None:
        return

    deleted_name = products[selected_index]["name"]
    del products[selected_index]
    recalculate_all_metrics()
    refresh_product_tree()

    if feedback_label is not None:
        if products:
            feedback_label.config(text=f"Deleted product: {deleted_name}")
        else:
            feedback_label.config(text="Deleted last product. Save Data to keep the list empty.")

    show_analysis_text("")
    update_status_label("")


def recalculate_all_metrics():
    """
    Recalculate metrics for every product in-place.
    Keeps score/status values consistent after add/delete/load events.
    """
    global products
    products = recalculate_all_products(products)



def apply_scenario_to_product(product_index: int, new_price: float, new_quantity: int, scenario_result: dict, popup):
    """
    Apply a tested scenario to the saved product list.
    """
    product = products[product_index]
    if not confirm_risky_product_change(product, scenario_result, popup):
        return

    products[product_index]["price"] = float(new_price)
    products[product_index]["quantity"] = int(new_quantity)
    recalculate_all_metrics()
    refresh_product_tree()

    if product_tree is not None:
        product_tree.selection_set(str(product_index))
        product_tree.focus(str(product_index))

    analyze_selected()

    if feedback_label is not None:
        feedback_label.config(text=f"Applied tested scenario to {products[product_index]['name']}.")

    popup.destroy()


def run_what_if(product_index: int, new_price_entry, new_quantity_entry, result_widget, apply_button=None, popup=None):
    """
    Execute what-if calculation and show results in popup.
    """
    try:
        new_price = safe_parse_float(
            new_price_entry.get(),
            "Please enter a test selling price.",
            "Please enter a valid number for test selling price."
        )
        new_quantity = safe_parse_int(
            new_quantity_entry.get(),
            "Please enter an expected quantity sold.",
            "Please enter a valid whole number for expected quantity sold."
        )

        if new_price < 0 or new_quantity < 0:
            raise ValueError("Test selling price and expected quantity cannot be negative.")

        product = products[product_index]
        result = what_if_analysis(product, products, new_price, new_quantity)

        original_profit = float(product.get("profit", 0))
        profit_change = float(result.get("profit", 0)) - original_profit

        result_profit = float(result.get("profit", 0))
        result_profit_text = f"-${abs(result_profit):.2f}" if result_profit < 0 else f"${result_profit:.2f}"
        profit_change_text = f"-${abs(profit_change):.2f}" if profit_change < 0 else f"${profit_change:.2f}"

        result_text = (
            f"=== WHAT-IF ANALYSIS ===\n\n"
            f"Product          : {result.get('name', '')}\n"
            f"New Revenue      : ${result.get('revenue', 0):.2f}\n"
            f"New Profit       : {result_profit_text}\n"
            f"New Margin       : {result.get('margin', 0):.2f}%\n"
            f"New Score        : {result.get('score', 0)}/100\n"
            f"New Decision     : {result.get('status', 'Unknown')}\n"
            f"Scenario Tip     : {result.get('scenario_recommendation', 'No scenario recommendation available.')}\n"
            f"Profit Change    : {profit_change_text}\n"
        )

        result_widget.config(state="normal")
        result_widget.delete("1.0", tk.END)
        result_widget.insert(tk.END, result_text)
        result_widget.config(state="disabled")

        if apply_button is not None and popup is not None:
            apply_button.config(
                state="normal",
                command=lambda: apply_scenario_to_product(product_index, new_price, new_quantity, result, popup)
            )

    except ValueError as error:
        title = "Missing Input" if "Please enter" in str(error) else "Invalid Input"
        parent_window = result_widget.winfo_toplevel()
        messagebox.showwarning(title, str(error), parent=parent_window)
        parent_window.after(50, lambda: focus_popup_entry(parent_window, new_price_entry))


def open_what_if_window():
    """
    Open popup window for what-if analysis.
    """
    selected_index = get_selected_product_index()
    if selected_index is None:
        return

    product = products[selected_index]

    popup = tk.Toplevel(root)
    popup.title("Scenario Planner")
    popup.geometry("860x500")
    popup.minsize(800, 460)
    popup.configure(bg="#edf3f8")
    popup.transient(root)

    popup_frame = tk.Frame(popup, padx=18, pady=16, bg="#ffffff")
    popup_frame.pack(fill="both", expand=True)
    popup_frame.columnconfigure(0, weight=0)
    popup_frame.columnconfigure(1, weight=1)
    popup_frame.rowconfigure(2, weight=1)

    tk.Label(
        popup_frame,
        text=f"Scenario Planner for {product['name']}",
        font=("Segoe UI", 15, "bold"),
        justify="center",
        bg="#ffffff",
        fg="#0f3d56"
    ).grid(row=0, column=0, columnspan=2, pady=(4, 8), sticky="ew")
    tk.Label(
        popup_frame,
        text="Test a possible price and demand change before making a business decision.",
        wraplength=680,
        justify="center",
        fg="#5d6d7e",
        bg="#ffffff",
        font=("Segoe UI", 10)
    ).grid(row=1, column=0, columnspan=2, pady=(0, 14), sticky="ew")

    input_panel = tk.Frame(popup_frame, bg="#f8fbfd", padx=16, pady=16, highlightthickness=1, highlightbackground="#cfe0e8")
    input_panel.grid(row=2, column=0, sticky="ns", padx=(0, 16))

    result_panel = tk.Frame(popup_frame, bg="#ffffff")
    result_panel.grid(row=2, column=1, sticky="nsew")
    result_panel.columnconfigure(0, weight=1)
    result_panel.rowconfigure(1, weight=1)

    tk.Label(input_panel, text="Scenario Inputs", bg="#f8fbfd", fg="#0f3d56", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 12))

    tk.Label(input_panel, text="New Selling Price", bg="#f8fbfd", fg="#17202a", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(4, 3))
    new_price_entry = tk.Entry(
        input_panel,
        width=24,
        justify="center",
        relief="flat",
        bd=0,
        bg="#ffffff",
        font=("Segoe UI", 10),
        highlightthickness=1,
        highlightbackground="#cfe0e8",
        highlightcolor="#1f7a8c"
    )
    new_price_entry.insert(0, str(product["price"]))
    new_price_entry.pack(fill="x", pady=(0, 12))

    tk.Label(input_panel, text="New Quantity", bg="#f8fbfd", fg="#17202a", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(2, 3))
    new_quantity_entry = tk.Entry(
        input_panel,
        width=24,
        justify="center",
        relief="flat",
        bd=0,
        bg="#ffffff",
        font=("Segoe UI", 10),
        highlightthickness=1,
        highlightbackground="#cfe0e8",
        highlightcolor="#1f7a8c"
    )
    new_quantity_entry.insert(0, str(product["quantity"]))
    new_quantity_entry.pack(fill="x", pady=(0, 16))

    tk.Label(
        input_panel,
        text="Margin guide: aim near 40% when possible.\nUnder 10% is risky unless demand is very high.",
        bg="#f8fbfd",
        fg="#5d6d7e",
        font=("Segoe UI", 9),
        justify="left",
        wraplength=210
    ).pack(anchor="w", pady=(0, 10))

    apply_button = tk.Button(
        input_panel,
        text="Apply Tested Scenario",
        state="disabled",
        width=18,
        bg="#2e8b57",
        fg="white",
        disabledforeground="#d9e5ea",
        activebackground="#256f46",
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=10,
        pady=7,
        cursor="hand2"
    )

    run_button = tk.Button(
        input_panel,
        text="Test Scenario",
        width=18,
        command=lambda: run_what_if(
            selected_index,
            new_price_entry,
            new_quantity_entry,
            result_widget,
            apply_button,
            popup
        ),
        bg="#f2a541",
        fg="#17202a",
        activebackground="#d98c25",
        activeforeground="#17202a",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=10,
        pady=7,
        cursor="hand2"
    )
    run_button.pack(fill="x", pady=(4, 6))
    apply_button.pack(fill="x", pady=(0, 0))

    tk.Label(
        result_panel,
        text="Scenario Result",
        bg="#ffffff",
        fg="#0f3d56",
        font=("Segoe UI", 12, "bold")
    ).grid(row=0, column=0, sticky="w", pady=(0, 8))

    result_widget = tk.Text(
        result_panel,
        height=13,
        width=56,
        state="disabled",
        wrap="word",
        bg="#fbfdfe",
        fg="#17202a",
        relief="flat",
        bd=0,
        padx=10,
        pady=8,
        font=("Consolas", 10),
        highlightthickness=1,
        highlightbackground="#cfe0e8",
        highlightcolor="#1f7a8c"
    )
    result_widget.grid(row=1, column=0, sticky="nsew")


def run_break_even(fixed_cost_entry, result_label):
    """
    Run break-even calculation and show result in popup.
    """
    try:
        fixed_cost = safe_parse_float(
            fixed_cost_entry.get(),
            "Please enter the total fixed cost.",
            "Please enter a valid number for total fixed cost."
        )
        if fixed_cost < 0:
            raise ValueError("Fixed cost cannot be negative.")

        current_units = int(sum(float(item.get("quantity", 0)) for item in products))
        required_units = business_break_even(products, fixed_cost)

        if required_units is None:
            result_label.config(
                text=(
                    "Break-even is not possible with the current overall product mix.\n"
                    "This uses all products together, not just one product."
                )
            )
        elif current_units >= required_units:
            result_label.config(
                text=(
                    "Your business is already covering its fixed costs.\n"
                    "This uses all products together, not just one product."
                )
            )
        else:
            additional_units = required_units - current_units
            result_label.config(
                text=(
                    "Your business has not yet reached break-even.\n"
                    f"Estimated additional units needed: {additional_units}\n"
                    "This uses all products together, not just one product."
                )
            )

    except ValueError as error:
        title = "Missing Input" if "Please enter" in str(error) else "Invalid Input"
        parent_window = result_label.winfo_toplevel()
        messagebox.showwarning(title, str(error), parent=parent_window)
        parent_window.after(50, lambda: focus_popup_entry(parent_window, fixed_cost_entry))


def focus_popup_entry(popup, entry):
    """
    Bring a popup forward and return keyboard focus to an entry widget.
    """
    try:
        popup.lift()
        popup.focus_force()
        entry.focus_force()
        entry.selection_range(0, tk.END)
    except tk.TclError:
        return


def open_break_even_window():
    """
    Open popup window for break-even analysis.
    """
    if not products:
        messagebox.showwarning("No Products", "Please add at least one product first.")
        return

    popup = tk.Toplevel(root)
    popup.title("Break-Even Planner")
    popup.geometry("460x320")
    popup.configure(bg="#edf3f8")
    popup.transient(root)

    popup_frame = tk.Frame(popup, padx=18, pady=16, bg="#ffffff")
    popup_frame.pack(fill="both", expand=True)

    tk.Label(
        popup_frame,
        text="Break-Even Planner",
        font=("Segoe UI", 15, "bold"),
        justify="center",
        bg="#ffffff",
        fg="#0f3d56"
    ).pack(pady=(4, 8))
    tk.Label(
        popup_frame,
        text="Break-even estimates when sales cover fixed costs and profit begins.",
        wraplength=390,
        justify="center",
        fg="#5d6d7e",
        bg="#ffffff",
        font=("Segoe UI", 10)
    ).pack(pady=(0, 8))

    tk.Label(popup_frame, text="Enter Fixed Cost", bg="#ffffff", fg="#17202a", font=("Segoe UI", 10, "bold")).pack(pady=(4, 2))
    fixed_cost_entry = tk.Entry(
        popup_frame,
        width=24,
        justify="center",
        relief="flat",
        bd=0,
        bg="#f8fbfd",
        font=("Segoe UI", 10),
        highlightthickness=1,
        highlightbackground="#cfe0e8",
        highlightcolor="#1f7a8c"
    )
    fixed_cost_entry.pack(pady=(0, 6))

    tk.Label(
        popup_frame,
        text="This uses all products together, not just one product.",
        wraplength=390,
        justify="center",
        fg="#5d6d7e",
        bg="#ffffff",
        font=("Segoe UI", 10)
    ).pack(pady=(2, 8))

    result_label = tk.Label(popup_frame, text="", wraplength=360, justify="center", bg="#ffffff", fg="#17202a", font=("Segoe UI", 10, "bold"))
    result_label.pack(fill="x", pady=(8, 10))

    break_even_button = tk.Button(
        popup_frame,
        text="Calculate Break-Even",
        width=22,
        command=lambda: run_break_even(fixed_cost_entry, result_label),
        bg="#1f7a8c",
        fg="white",
        activebackground="#17606f",
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=10,
        pady=7,
        cursor="hand2"
    )
    break_even_button.pack(pady=(0, 4), anchor="center")


def load_demo_business():
    """Load sample USYD campus products for a quick live demo."""
    global products

    products = get_campus_demo_products()
    recalculate_all_metrics()
    refresh_product_tree()
    show_score_guide()

    if feedback_label is not None:
        feedback_label.config(text="Loaded USYD campus demo business.")


def export_business_report():
    """Export business reports through the reports module."""
    if not products:
        messagebox.showwarning("No Products", "Please add or load products first.")
        return

    recalculate_all_metrics()

    try:
        report_path, html_report_path = export_business_reports(products, BASE_DIR)
        html_report_url = "file:///" + os.path.abspath(html_report_path).replace("\\", "/")
        webbrowser.open_new_tab(html_report_url)

        messagebox.showinfo(
            "Export Complete",
            "Reports saved as:\n"
            f"{report_path}\n\n"
            f"{html_report_path}\n\n"
            "The HTML report has also been opened in your browser."
        )
    except (OSError, ValueError):
        messagebox.showerror("Export Error", "The business report could not be saved.")


def build_gui():
    """
    Build the main Tkinter GUI.
    """
    global root
    global name_entry, cost_entry, price_entry, qty_entry
    global feedback_label, product_tree, analysis_text, status_label
    global dashboard_value_labels
    global product_form_title, submit_product_button

    action_btn_width = 21
    list_btn_width = 15

    bg_color = "#edf3f8"
    panel_color = "#ffffff"
    header_color = "#0f3d56"
    primary_color = "#1f7a8c"
    primary_hover = "#17606f"
    success_color = "#2e8b57"
    warning_color = "#f2a541"
    danger_color = "#c94c4c"
    text_color = "#17202a"
    muted_color = "#5d6d7e"
    border_color = "#bfd3df"
    font_family = "Segoe UI"

    root = tk.Tk()
    root.title("ProfitPilot: Campus Business Simulator")
    root.geometry("1100x780")
    root.minsize(1000, 700)
    root.configure(bg=bg_color)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Profit.Treeview",
        background=panel_color,
        fieldbackground=panel_color,
        foreground=text_color,
        rowheight=28,
        bordercolor=border_color,
        borderwidth=0,
        font=(font_family, 10)
    )
    style.configure(
        "Profit.Treeview.Heading",
        background="#d8e8ef",
        foreground=header_color,
        font=(font_family, 10, "bold"),
        relief="flat"
    )
    style.map("Profit.Treeview", background=[("selected", primary_color)], foreground=[("selected", "white")])

    def make_button(parent, text, command, bg=primary_color, hover=primary_hover, fg="white", width=None):
        """
        Create a flat colored button with simple hover feedback.
        """
        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground="white",
            font=(font_family, 10, "bold"),
            relief="flat",
            bd=0,
            padx=10,
            pady=7,
            cursor="hand2"
        )
        button.bind("<Enter>", lambda event: button.config(bg=hover))
        button.bind("<Leave>", lambda event: button.config(bg=bg))
        return button

    # Header
    header_frame = tk.Frame(root, padx=12, pady=16, bg=header_color)
    header_frame.pack(fill="x")

    tk.Label(
        header_frame,
        text="ProfitPilot: Campus Business Simulator",
        font=(font_family, 22, "bold"),
        bg=header_color,
        fg="white",
        justify="center",
        anchor="center"
    ).pack(fill="x")

    tk.Label(
        header_frame,
        text="Test a USYD student side-hustle and discover what actually makes profit",
        font=(font_family, 11),
        bg=header_color,
        fg="#d6eef5",
        justify="center",
        anchor="center"
    ).pack(fill="x", pady=(2, 0))

    # Dashboard summary cards
    dashboard_frame = tk.Frame(root, padx=18, pady=6, bg=bg_color)
    dashboard_frame.pack(fill="x", pady=(4, 0))
    for column in range(4):
        dashboard_frame.columnconfigure(column, weight=1)

    dashboard_value_labels = {}

    def create_dashboard_card(parent, column, icon, title, value_key, accent_color):
        card = tk.Frame(
            parent,
            bg="#f8fbfd",
            padx=14,
            pady=8,
            highlightthickness=1,
            highlightbackground="#d7e6ed"
        )
        card.grid(row=0, column=column, sticky="ew", padx=6)

        accent = tk.Frame(card, bg=accent_color, width=5)
        accent.pack(side="left", fill="y", padx=(0, 12))

        text_area = tk.Frame(card, bg="#f8fbfd")
        text_area.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_area,
            text=icon,
            bg="#f8fbfd",
            fg=accent_color,
            font=(font_family, 18, "bold")
        ).pack(anchor="w")

        tk.Label(
            text_area,
            text=title,
            bg="#f8fbfd",
            fg=muted_color,
            font=(font_family, 9, "bold")
        ).pack(anchor="w", pady=(2, 0))

        value_label = tk.Label(
            text_area,
            text="--",
            bg="#f8fbfd",
            fg=header_color,
            font=(font_family, 13, "bold"),
            wraplength=210,
            justify="left"
        )
        value_label.pack(anchor="w", pady=(5, 0))
        dashboard_value_labels[value_key] = value_label

    create_dashboard_card(dashboard_frame, 0, "#", "PRODUCTS", "products", primary_color)
    create_dashboard_card(dashboard_frame, 1, "$", "REVENUE", "revenue", "#2563eb")
    create_dashboard_card(dashboard_frame, 2, "+", "PROFIT", "profit", success_color)
    create_dashboard_card(dashboard_frame, 3, "#1", "TOP PRODUCT", "top", warning_color)

    tk.Label(
        root,
        text="Score guide: 40% profit, 40% margin, 20% demand. Use it to compare products quickly, not as a strict accounting rule.",
        bg=bg_color,
        fg=muted_color,
        font=(font_family, 9),
        anchor="center",
        justify="center"
    ).pack(fill="x", padx=18, pady=(0, 4))

    # Main content frame
    main_frame = tk.Frame(root, padx=18, pady=6, bg=bg_color)
    main_frame.pack(fill="both", expand=True)

    # Configure 3 columns
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=2)
    main_frame.columnconfigure(2, weight=1)
    main_frame.rowconfigure(0, weight=1)

    # -------------------------
    # Input Panel
    # -------------------------
    input_frame = tk.LabelFrame(
        main_frame,
        text="Product Entry",
        padx=14,
        pady=12,
        bg=panel_color,
        fg=header_color,
        font=(font_family, 11, "bold"),
        bd=0,
        relief="flat",
        highlightthickness=0
    )
    input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=4)
    input_frame.columnconfigure(0, weight=1)

    product_form_title = tk.Label(input_frame, text="Add Product", bg=panel_color, fg=header_color, font=(font_family, 13, "bold"))
    product_form_title.grid(row=0, column=0, sticky="w", pady=(0, 10))

    tk.Label(input_frame, text="Product Name", bg=panel_color, fg=text_color, font=(font_family, 10, "bold")).grid(row=1, column=0, sticky="w")
    name_entry = tk.Entry(input_frame, width=25, relief="flat", bd=0, bg="#f8fbfd", font=(font_family, 10), highlightthickness=1, highlightbackground="#cfe0e8", highlightcolor=primary_color)
    name_entry.grid(row=2, column=0, pady=5, sticky="ew")

    tk.Label(input_frame, text="Cost Price", bg=panel_color, fg=text_color, font=(font_family, 10, "bold")).grid(row=3, column=0, sticky="w")
    cost_entry = tk.Entry(input_frame, width=25, relief="flat", bd=0, bg="#f8fbfd", font=(font_family, 10), highlightthickness=1, highlightbackground="#cfe0e8", highlightcolor=primary_color)
    cost_entry.grid(row=4, column=0, pady=5, sticky="ew")

    tk.Label(input_frame, text="Selling Price", bg=panel_color, fg=text_color, font=(font_family, 10, "bold")).grid(row=5, column=0, sticky="w")
    price_entry = tk.Entry(input_frame, width=25, relief="flat", bd=0, bg="#f8fbfd", font=(font_family, 10), highlightthickness=1, highlightbackground="#cfe0e8", highlightcolor=primary_color)
    price_entry.grid(row=6, column=0, pady=5, sticky="ew")

    tk.Label(input_frame, text="Expected Quantity", bg=panel_color, fg=text_color, font=(font_family, 10, "bold")).grid(row=7, column=0, sticky="w")
    qty_entry = tk.Entry(input_frame, width=25, relief="flat", bd=0, bg="#f8fbfd", font=(font_family, 10), highlightthickness=1, highlightbackground="#cfe0e8", highlightcolor=primary_color)
    qty_entry.grid(row=8, column=0, pady=5, sticky="ew")

    submit_product_button = make_button(input_frame, "Add Product", add_product, bg=success_color, hover="#256f46", width=action_btn_width)
    submit_product_button.grid(row=9, column=0, pady=(14, 5), sticky="ew")
    make_button(input_frame, "Clear / Cancel", clear_fields, bg="#64748b", hover="#475569", width=action_btn_width).grid(row=10, column=0, pady=5, sticky="ew")
    make_button(input_frame, "Load Campus Demo", load_demo_business, bg=warning_color, hover="#d98c25", fg="#17202a", width=action_btn_width).grid(row=11, column=0, pady=5, sticky="ew")

    feedback_label = tk.Label(input_frame, text="", fg=primary_color, bg=panel_color, wraplength=230, justify="left", font=(font_family, 10, "bold"))
    feedback_label.grid(row=12, column=0, pady=(10, 4), sticky="w")

    # -------------------------
    # Product List Panel
    # -------------------------
    list_frame = tk.LabelFrame(
        main_frame,
        text="Product Performance",
        padx=14,
        pady=12,
        bg=panel_color,
        fg=header_color,
        font=(font_family, 11, "bold"),
        bd=0,
        relief="flat",
        highlightthickness=0
    )
    list_frame.grid(row=0, column=1, sticky="nsew", padx=12, pady=4)

    columns = ("name", "cost", "price", "quantity", "profit", "score", "status")
    product_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10, selectmode='browse', style="Profit.Treeview")

    product_tree.heading("name", text="Name")
    product_tree.heading("cost", text="Cost")
    product_tree.heading("price", text="Price")
    product_tree.heading("quantity", text="Qty")
    product_tree.heading("profit", text="Profit")
    product_tree.heading("score", text="Score")
    product_tree.heading("status", text="Decision")

    product_tree.column("name", width=170)
    product_tree.column("cost", width=65, anchor="center")
    product_tree.column("price", width=65, anchor="center")
    product_tree.column("quantity", width=55, anchor="center")
    product_tree.column("profit", width=80, anchor="center")
    product_tree.column("score", width=75, anchor="center")
    product_tree.column("status", width=130, anchor="center")

    product_tree.pack(fill="both", expand=True, pady=(6, 10))

    list_button_frame = tk.Frame(list_frame, bg=panel_color)
    list_button_frame.pack(fill="x", pady=(2, 10))

    make_button(list_button_frame, "Load Data", load_products, bg=primary_color, hover=primary_hover, width=10).pack(side="left", padx=3)
    make_button(list_button_frame, "Save Data", save_products, bg=success_color, hover="#256f46", width=10).pack(side="left", padx=3)
    make_button(list_button_frame, "Edit", start_edit_selected, bg="#f2a541", hover="#d98c25", fg="#17202a", width=9).pack(side="left", padx=3)
    make_button(list_button_frame, "Export", export_business_report, bg=success_color, hover="#256f46", width=9).pack(side="left", padx=3)
    make_button(list_button_frame, "Delete", delete_selected, bg=danger_color, hover="#a63d3d", width=9).pack(side="left", padx=3)

    tk.Label(list_frame, text="Select a product to view its recommendation", bg=panel_color, fg=muted_color, font=(font_family, 10)).pack(anchor="w", pady=(2, 2))

    # -------------------------
    # Analysis Panel
    # -------------------------
    analysis_frame = tk.LabelFrame(
        main_frame,
        text="Business Insights",
        padx=14,
        pady=12,
        bg=panel_color,
        fg=header_color,
        font=(font_family, 11, "bold"),
        bd=0,
        relief="flat",
        highlightthickness=0
    )
    analysis_frame.grid(row=0, column=2, sticky="nsew", padx=(12, 0), pady=4)

    status_label = tk.Label(
        analysis_frame,
        text="Decision:",
        font=(font_family, 13, "bold"),
        bg=panel_color,
        fg=text_color
    )
    status_label.pack(anchor="w", pady=(4, 8))

    analysis_text = tk.Text(
        analysis_frame,
        height=10,
        width=35,
        state="disabled",
        wrap="word",
        bg="#fbfdfe",
        fg=text_color,
        relief="flat",
        bd=0,
        padx=10,
        pady=10,
        font=(font_family, 10),
        highlightthickness=1,
        highlightbackground="#cfe0e8",
        highlightcolor=primary_color
    )
    analysis_text.pack(fill="both", expand=True, pady=(0, 5))
    ttk.Separator(analysis_frame, orient="horizontal").pack(fill="x", pady=(2, 5))
    guide_frame = tk.Frame(analysis_frame, bg=panel_color)
    guide_frame.pack(fill="x", pady=(0, 6))
    guide_frame.columnconfigure(0, weight=1)

    tk.Label(
        guide_frame,
        text="Score compares profit, margin, and customer demand to support business decisions.",
        wraplength=300,
        justify="left",
        fg=muted_color,
        bg=panel_color,
        font=(font_family, 10)
    ).grid(row=0, column=0, sticky="w")

    make_button(
        guide_frame,
        "Decision Guide",
        show_score_guide,
        bg="#64748b",
        hover="#475569"
    ).grid(row=0, column=1, sticky="e", padx=(8, 0))

    analysis_button_frame = tk.Frame(analysis_frame, bg=panel_color)
    analysis_button_frame.pack(fill="x", pady=(0, 6))
    analysis_button_frame.columnconfigure(0, weight=1)
    analysis_button_frame.columnconfigure(1, weight=1)

    make_button(analysis_button_frame, "+ Product Snapshot", analyze_selected, bg=primary_color, hover=primary_hover).grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=2)
    make_button(analysis_button_frame, "Business Summary", analyze_all, bg="#2563eb", hover="#1d4ed8").grid(row=0, column=1, sticky="ew", padx=(4, 0), pady=2)
    make_button(analysis_button_frame, "Test Scenario", open_what_if_window, bg=warning_color, hover="#d98c25", fg="#17202a").grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=2)
    make_button(analysis_button_frame, "Break-Even Plan", open_break_even_window, bg="#8b5cf6", hover="#7c3aed").grid(row=1, column=1, sticky="ew", padx=(4, 0), pady=2)
    make_button(analysis_button_frame, "Export Business Report", export_business_report, bg=success_color, hover="#256f46").grid(row=2, column=0, columnspan=2, sticky="ew", pady=(3, 0))

    # Footer
    footer_frame = tk.Frame(root, padx=18, pady=12, bg=bg_color)
    footer_frame.pack(fill="x")

    make_button(footer_frame, "Exit", root.destroy, bg="#334155", hover="#1e293b", width=14).pack(side="right")

    # Auto-load saved data
    load_products(show_message=False)

    root.mainloop()


if __name__ == "__main__":
    build_gui()

