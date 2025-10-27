"""
Inventory Management System

This module provides basic inventory management functionalities such as
adding, removing, and checking items in stock. It includes safe file handling,
input validation, and logging of actions.
"""

import json
from datetime import datetime
import logging
from typing import Optional, List

# Configure logging
logging.basicConfig(
    filename="inventory.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global variable
stock_data = {}


def add_item(
    item: str = "default",
    qty: int = 0,
    logs: Optional[List[str]] = None
) -> None:
    """Add the specified quantity of an item to the stock."""
    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning(
            "Invalid data types for add_item: item=%s, qty=%s", item, qty
        )
        return

    if logs is None:
        logs = []

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s to inventory.", qty, item)


def remove_item(item: str, qty: int) -> None:
    """Remove a specified quantity of an item from the stock."""
    try:
        if item in stock_data:
            stock_data[item] -= qty
            if stock_data[item] <= 0:
                del stock_data[item]
                logging.info(
                    "Removed %s completely from inventory.", item
                )
            else:
                logging.info("Removed %d of %s from inventory.", qty, item)
        else:
            logging.warning(
                "Attempted to remove non-existent item: %s", item
            )
    except (KeyError, TypeError) as err:
        logging.error("Error removing item %s: %s", item, err)


def get_qty(item: str) -> Optional[int]:
    """Return the quantity of a specific item in stock."""
    return stock_data.get(item)


def load_data(file: str = "inventory.json") -> dict:
    """Load inventory data from a JSON file and return it."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        logging.info("Inventory data loaded successfully from %s", file)
        return data
    except FileNotFoundError:
        logging.warning(
            "File %s not found. Starting with an empty inventory.", file
        )
        return {}
    except json.JSONDecodeError as err:
        logging.error("Error decoding JSON file %s: %s", file, err)
        return {}


def save_data(file: str = "inventory.json") -> None:
    """Save inventory data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Inventory data saved successfully to %s", file)
    except OSError as err:
        logging.error("Error saving data to %s: %s", file, err)


def print_data() -> None:
    """Display all items and their quantities."""
    print("\nItems Report:")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold: int = 5) -> List[str]:
    """Return a list of items that are below the given threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Main execution block for inventory management demonstration."""
    logs = []

    add_item("apple", 10, logs)
    add_item("banana", 2, logs)
    add_item("orange", 1, logs)
    remove_item("apple", 3)
    remove_item("mango", 1)  # Non-existent item test

    apple_qty = get_qty("apple")
    if apple_qty is not None:
        print(f"Apple stock: {apple_qty}")
    else:
        print("Apple not found in inventory.")

    print(f"Low items: {check_low_items()}")

    save_data()

    # Load data safely without using global keyword
    loaded_data = load_data()
    stock_data.clear()
    stock_data.update(loaded_data)

    print_data()
    print("Note: eval() removed for security reasons.")


if __name__ == "__main__":
    main()
