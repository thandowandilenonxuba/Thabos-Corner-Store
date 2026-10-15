"""
database.py
------------
Task 3: Build a relational database from your cleaned data.

This module covers KM-04 topics: Introduction to Databases (DBMS,
components, characteristics) and Structured Query Language (SQL).

You will use Python's built-in `sqlite3` module — no extra install
needed. SQLite stores the whole database in a single file, which makes
it perfect for a student project (and easy to include as evidence).

By the end of this file you must be able to:
  1. Create a database file (store.db) with two related tables.
  2. Insert your cleaned data into those tables.
  3. Run at least FIVE meaningful SQL queries against the data,
     including at least one JOIN and one aggregation (SUM, COUNT, AVG).
"""

import sqlite3


def get_connection(db_path: str = "store.db") -> sqlite3.Connection:
    """
    Open (and create, if needed) the SQLite database file.

    Returns:
        an open sqlite3.Connection
    """
    conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = ON")
return conn


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create the `products` and `sales` tables if they don't already exist.
    """

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            unit_price REAL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id TEXT PRIMARY KEY,
            product_id TEXT,
            quantity INTEGER,
            sale_date TEXT,
            payment_method TEXT,
            customer_type TEXT,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    conn.commit()


def insert_products(conn: sqlite3.Connection, products_df) -> None:
    """
    Insert every row of the cleaned products DataFrame into the
    products table.
    """

    for row in products_df.itertuples(index=False):
        conn.execute(
            """
            INSERT INTO products
            (product_id, product_name, category, unit_price)
            VALUES (?, ?, ?, ?)
            """,
            (
                row.product_id,
                row.product_name,
                row.category,
                row.unit_price
            )
        )

    conn.commit()


def insert_sales(conn: sqlite3.Connection, sales_df) -> None:
    """
    Insert every row of the cleaned sales DataFrame into the sales table.
    """

    for row in sales_df.itertuples(index=False):
        conn.execute(
            """
            INSERT INTO sales
            (sale_id, product_id, quantity, sale_date, payment_method, customer_type)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row.sale_id,
                row.product_id,
                row.quantity,
                row.sale_date,
                row.payment_method,
                row.customer_type
            )
        )

    conn.commit()


# ---------------------------------------------------------------------
# SQL QUERIES — write at least FIVE for your project.
# Three are started for you below; you must complete them and add TWO
# more of your own that answer a business question you find interesting.
# ---------------------------------------------------------------------

def query_total_revenue_per_product(conn: sqlite3.Connection):
    """
    Return each product's name and its total revenue
    (quantity * unit_price), highest revenue first.
    """

    sql = """
        SELECT
            products.product_name,
            SUM(sales.quantity * products.unit_price) AS total_revenue
        FROM sales
        JOIN products
            ON sales.product_id = products.product_id
        GROUP BY products.product_id, products.product_name
        ORDER BY total_revenue DESC
    """

    return conn.execute(sql).fetchall()


def query_best_selling_product(conn: sqlite3.Connection):
    """
    Return the single product with the highest total quantity sold.
    """

    sql = """
        SELECT
            products.product_name,
            SUM(sales.quantity) AS total_quantity_sold
        FROM sales
        JOIN products
            ON sales.product_id = products.product_id
        GROUP BY products.product_id, products.product_name
        ORDER BY total_quantity_sold DESC
        LIMIT 1
    """

    return conn.execute(sql).fetchall()


def query_sales_by_payment_method(conn: sqlite3.Connection):
    """
    Return the number of sales transactions per payment method.
    """

    sql = """
        SELECT
            payment_method,
            COUNT(*) AS total_transactions
        FROM sales
        GROUP BY payment_method
        ORDER BY total_transactions DESC
    """

    return conn.execute(sql).fetchall()


def query_custom_one(conn: sqlite3.Connection):
    """
    Business question: Which product category generates the most revenue?
    """

    sql = """
        SELECT
            products.category,
            SUM(sales.quantity * products.unit_price) AS total_revenue
        FROM sales
        JOIN products
            ON sales.product_id = products.product_id
        GROUP BY products.category
        ORDER BY total_revenue DESC
    """

    return conn.execute(sql).fetchall()


def query_custom_two(conn: sqlite3.Connection):
    """
    Business question: How many sales transactions were made to each
    customer type during January 2026?
    """

    sql = """
        SELECT
            customer_type,
            COUNT(*) AS total_transactions,
            SUM(quantity) AS total_quantity_sold
        FROM sales
        WHERE sale_date >= '2026-01-01'
          AND sale_date < '2026-02-01'
        GROUP BY customer_type
        ORDER BY total_transactions DESC
    """

    return conn.execute(sql).fetchall()
