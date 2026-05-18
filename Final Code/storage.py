"""JSON storage helpers for ProfitPilot.

The GUI decides when to show success or error dialogs. This module only reads
and writes product data, keeping file I/O separate from interface code.
"""

import json
import os


def save_products_to_file(products: list, data_file: str) -> None:
    """Save the product list to a JSON file."""
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4)


def load_products_from_file(data_file: str) -> list:
    """Load products from JSON and validate that the file contains a list."""
    if not os.path.exists(data_file):
        raise FileNotFoundError(data_file)

    with open(data_file, "r", encoding="utf-8") as file:
        loaded_products = json.load(file)

    if not isinstance(loaded_products, list):
        raise ValueError("Saved product data must be a list.")

    return loaded_products
