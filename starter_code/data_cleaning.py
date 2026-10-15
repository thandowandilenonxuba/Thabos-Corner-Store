"""
data_cleaning.py
-----------------
Task 2: Load the raw CSV files and clean them.

This module covers KM-04 topics: Introduction to Data (data types,
errors of omission) and Data in Spreadsheets.

The raw files in data/products.csv and data/sales.csv contain REAL
data-quality problems on purpose, so you get practice fixing them:

  products.csv issues to find and fix:
    - Some products are missing a unit_price
    - One product is missing its product_name
    - Category text is inconsistently capitalised (e.g. "beverages" vs "Beverages")
    - One exact duplicate row

  sales.csv issues to find and fix:
    - sale_date is written in at least FOUR different formats
    - Some rows have a missing sale_date (an error of omission)
    - Some rows have a missing quantity
    - Some rows have a missing payment_method
    - A few rows reference a product_id that does not exist in products.csv
    - One exact duplicate row

You must handle every one of these before the data moves on to the
database in database.py. Document the decisions you make (e.g. "rows
with a missing sale_date were dropped because we cannot analyse sales
trends without a date") in your README findings section.
"""

import pandas as pd


def load_raw_data(products_path: str, sales_path: str):
    """
    Load the two raw CSV files into pandas DataFrames.

    Args:
        products_path: file path to products.csv
        sales_path: file path to sales.csv

    Returns:
        (products_df, sales_df) tuple of pandas DataFrames, UNCLEANED.
    """
    products_df = pd.read_csv(products_path)
    sales_df = pd.read_csv(sales_path)

    return products_df, sales_df

def clean_products(products_df: "pd.DataFrame") -> "pd.DataFrame":
    """
    Clean the products DataFrame.

    Must handle:
        - Missing unit_price (decide: drop the row, or fill with a sensible
          value? Justify your choice in the README.)
        - Missing product_name (a product with no name is not usable data —
          what should happen to that row?)
        - Inconsistent category capitalisation (standardise to Title Case,
          e.g. "beverages" -> "Beverages")
        - Duplicate rows (remove them)

    Returns:
        A cleaned copy of the DataFrame. Do not modify products_df in place.
    """
    cleaned_df = products_df.copy()

    cleaned_df = cleaned_df.dropna(subset=["unit_price"])
    cleaned_df = cleaned_df.dropna(subset=["product_name"])

    cleaned_df["category"] = cleaned_df["category"].str.title()

    cleaned_df = cleaned_df.drop_duplicates()

    return cleaned_df


def clean_sales(sales_df: "pd.DataFrame", valid_product_ids) -> "pd.DataFrame":
    """
    Clean the sales DataFrame.

    Args:
        sales_df: the raw sales DataFrame
        valid_product_ids: a collection of product_id values that exist
            in the cleaned products table.

    Returns:
        A cleaned copy of the DataFrame with a standardised sale_date
        column and no missing values in quantity or product_id.
    """
    cleaned_df = sales_df.copy()

    # Remove exact duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Convert quantity to numeric
    cleaned_df["quantity"] = pd.to_numeric(
        cleaned_df["quantity"], errors="coerce"
    )

    # Fill missing payment methods with "Unknown"
    cleaned_df["payment_method"] = cleaned_df["payment_method"].fillna("Unknown")

    # Convert different date formats into one standard date
    date_formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y"
    ]

    parsed_dates = pd.Series(pd.NaT, index=cleaned_df.index)

    for date_format in date_formats:
        missing_dates = parsed_dates.isna()

        parsed_dates.loc[missing_dates] = pd.to_datetime(
            cleaned_df.loc[missing_dates, "sale_date"],
            format=date_format,
            errors="coerce"
        )

    cleaned_df["sale_date"] = parsed_dates

    # Remove rows with missing or invalid dates
    cleaned_df = cleaned_df.dropna(subset=["sale_date"])

    # Remove rows with missing quantity
    cleaned_df = cleaned_df.dropna(subset=["quantity"])

    # Keep only sales linked to valid products
    cleaned_df = cleaned_df[
        cleaned_df["product_id"].isin(valid_product_ids)
    ]

    # Convert dates to YYYY-MM-DD format
    cleaned_df["sale_date"] = cleaned_df["sale_date"].dt.strftime("%Y-%m-%d")

    return cleaned_df


def cleaning_summary(raw_df: "pd.DataFrame", clean_df: "pd.DataFrame", name: str) -> str:
    """
    Build a short, human-readable string summarising how many rows were
    removed during cleaning.
    """
    removed = len(raw_df) - len(clean_df)

    return f"{name}: {len(raw_df)} raw rows -> {len(clean_df)} clean rows ({removed} removed)"
