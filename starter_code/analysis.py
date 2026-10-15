"""
analysis.py
------------
Task 4: Programming logic — functions, loops, conditionals and arrays.

This module covers KM-05 topics: Programming Basics (data types,
conditionals, loops, arrays/lists, functions) and Introduction to
Algorithms.

IMPORTANT: For this file, use plain Python (for-loops, if/else,
lists and dictionaries) even where pandas could do it in one line.
The point of this section is to demonstrate the programming
fundamentals from KM-05, not just pandas shortcuts.
"""


def total_sales_records(sales_rows: list) -> int:
    """
    Count the total number of sales records using a loop.
    """

    count = 0

    for row in sales_rows:
        count += 1

    return count


def low_stock_alert(products_rows: list, threshold: int = 5) -> list:
    """
    Return product names that are marked as out of stock.
    """

    alerts = []

    for product in products_rows:
        if product["in_stock"] is False or product["in_stock"] == "False":
            alerts.append(product["product_name"])

    return alerts


def monthly_sales_trend(sales_rows: list) -> dict:
    """
    Calculate the total quantity sold for each month.
    """

    trend = {}

    for row in sales_rows:
        month = row["sale_date"][:7]

        if month in trend:
            trend[month] += row["quantity"]
        else:
            trend[month] = row["quantity"]

    return trend


def classify_transaction_size(quantity: int) -> str:
    """
    Classify a transaction based on the quantity purchased.
    """

    if quantity >= 5:
        return "Bulk"
    elif quantity >= 2:
        return "Multiple"
    elif quantity == 1:
        return "Single"
    else:
        return "Invalid"


def average_basket_size(sales_rows: list) -> float:
    """
    Calculate the average quantity per sale, rounded to 2 decimal places.
    """

    if not sales_rows:
        return 0.0

    total = 0

    for row in sales_rows:
        total += row["quantity"]

    return round(total / len(sales_rows), 2)
