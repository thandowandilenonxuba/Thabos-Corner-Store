# Thabo's Corner Store — Sales Insights System

## 1. Project Overview

This project develops a Python-based sales insights system for Thabo's Corner Store. It cleans product and sales data, stores the cleaned information in an SQLite relational database, performs SQL queries and business analysis, and generates charts to help the store understand its sales.

## 2. Technologies Used

- Python
- pandas
- SQLite and SQL
- matplotlib
- Visual Studio Code
- Git and GitHub

## 3. Project Structure

```text
Thabos_Corner_Store/
├── data/
│   ├── Products.csv
│   └── Sales.csv
└── starter_code/
    ├── analysis.py
    ├── data_cleaning.py
    ├── database.py
    ├── main.py
    ├── security.py
    ├── visualize.py
    ├── requirements.txt
    ├── README.md
    ├── PLAN.md
    ├── store.db
    ├── revenue_per_product.png
    └── monthly_trend.png
```

## 4. Installation and Running the System

Requirements: Python and pip installed.

1. Open a terminal in the `starter_code` directory.
2. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python main.py
   ```

4. Enter the demonstration password `letmein` when prompted.
5. The application loads and cleans the CSV files, creates or updates the database, performs analysis, and generates two charts.

The demonstration password is hardcoded for this student project. It must not be reused as a real account password.

## 5. Data Cleaning Decisions

The system cleans the supplied product and sales CSV files before storing their data.

### Products

- Raw product records: 16.
- Clean product records: 12.
- Records removed: 4.
- Rows with missing unit prices are removed because reliable revenue calculations require a price.
- Rows with missing product names are removed because products must be identifiable.
- Category names are converted to title case for consistent reporting.
- Duplicate rows are removed.

### Sales

- Raw sales records: 71.
- Clean sales records: 43.
- Records removed: 28.
- Exact duplicate rows are removed.
- Quantities are converted to numeric values; invalid or missing quantities are excluded.
- Missing payment methods are labelled `Unknown`.
- Dates are parsed from supported formats and standardized to `YYYY-MM-DD`.
- Dates written as `DD/MM/YYYY` or `DD-MM-YYYY` are interpreted as day-first. ISO dates such as `YYYY-MM-DD` and year-first dates such as `YYYY/MM/DD` are also supported.
- Rows with missing or invalid dates are removed.
- Sales referring to product IDs absent from the cleaned product data are removed.

**Data limitation:** Day-first interpretation is an assumption for ambiguous dates. Removing incomplete records can also exclude genuine sales. These decisions should be reviewed if the original records become available.

## 6. Database Design

The application uses SQLite and creates two related tables.

### Products table

- `product_id`: primary key.
- `product_name`: product name.
- `category`: product category.
- `unit_price`: selling price per unit.

### Sales table

- `sale_id`: primary key.
- `product_id`: reference to the products table.
- `quantity`: quantity sold.
- `sale_date`: date of sale.
- `payment_method`: payment method used.
- `customer_type`: customer classification.

The sales table contains a foreign-key relationship to `products.product_id`. The application uses parameterized SQL statements when inserting data.

## 7. SQL Queries

The project implements five business queries.

### Query 1: Revenue per product

```sql
SELECT products.product_name,
       SUM(sales.quantity * products.unit_price) AS total_revenue
FROM sales
JOIN products ON sales.product_id = products.product_id
GROUP BY products.product_id, products.product_name
ORDER BY total_revenue DESC;
```

Purpose: Calculates revenue per product and sorts products from highest to lowest revenue.

### Query 2: Best-selling product by quantity

```sql
SELECT products.product_name,
       SUM(sales.quantity) AS total_quantity_sold
FROM sales
JOIN products ON sales.product_id = products.product_id
GROUP BY products.product_id, products.product_name
ORDER BY total_quantity_sold DESC
LIMIT 1;
```

Purpose: Identifies the product with the highest total quantity sold.

### Query 3: Transactions by payment method

```sql
SELECT payment_method, COUNT(*) AS total_transactions
FROM sales
GROUP BY payment_method
ORDER BY total_transactions DESC;
```

Purpose: Counts transactions for each payment method.

### Query 4: Revenue by product category

```sql
SELECT products.category,
       SUM(sales.quantity * products.unit_price) AS total_revenue
FROM sales
JOIN products ON sales.product_id = products.product_id
GROUP BY products.category
ORDER BY total_revenue DESC;
```

Purpose: Compares revenue across product categories.

### Query 5: Customer types during January 2026

```sql
SELECT customer_type,
       COUNT(*) AS total_transactions,
       SUM(quantity) AS total_quantity_sold
FROM sales
WHERE sale_date >= '2026-01-01'
  AND sale_date < '2026-02-01'
GROUP BY customer_type
ORDER BY total_transactions DESC;
```

Purpose: Compares the number of transactions and quantity sold to each customer type during January 2026.

### Sample SQL result

The application's latest recorded revenue-per-product output included:

| Product | Revenue |
|---|---:|
| 5kg Maize Meal | R801.00 |
| Eggs (6 pack) | R364.00 |
| Bar One Chocolate | R224.00 |
| Sugar 1kg | R220.50 |
| Coca-Cola 500ml | R148.00 |
| Airtime Voucher R10 | R140.00 |
| Simba Chips 120g | R132.00 |
| Full Cream Milk 1L | R129.00 |
| Fanta Orange 500ml | R111.00 |
| Data Bundle 1GB | R98.00 |
| Coca-Cola 500ml | R74.00 |
| White Bread 700g | R48.00 |

The remaining query results should be captured from the current database before final submission.

## 8. Python Analysis

The `analysis.py` module uses functions, loops, conditionals, lists, and dictionaries to:

- Count cleaned sales records.
- Identify products marked as out of stock.
- Summarize monthly quantities sold.
- Classify transaction quantities as Single, Multiple, Bulk, or Invalid.
- Calculate average quantity per sales record.

Latest recorded output:

- Total cleaned sales records: 43.
- Low-stock alert list: Data Bundle 1GB.
- Monthly quantities: January 2026 — 52; February 2026 — 44.
- Average quantity per sales record: 2.23.

The low-stock function flags products marked out of stock; it does not calculate stock levels from a numeric inventory balance.

## 9. Visualizations

The `visualize.py` module generates two PNG charts.

### Revenue per product

File: `revenue_per_product.png`

The bar chart compares total revenue across products. In the latest recorded results, 5kg Maize Meal generated the highest listed revenue at R801.00.

### Monthly sales trend

File: `monthly_trend.png`

The line chart displays monthly quantities sold. The latest recorded analysis showed 52 units in January 2026 and 44 in February 2026.

These charts summarize the cleaned dataset, not necessarily every original transaction.

## 10. Security Reflection: CIA Triad

Confidentiality means protecting information from unauthorized access. This project demonstrates a password gate before the main application runs. However, the demonstration password is hardcoded in the source code, so this is not suitable for a real business system. A production application should use secure credential storage, appropriate access controls, and stronger authentication practices.

Integrity means keeping data accurate and consistent. The project removes duplicate records, handles missing and invalid values, standardizes dates, and excludes sales linked to products that are not present in the cleaned product data. Primary keys and the sales-to-products foreign-key relationship support data consistency. The cleaning assumptions should still be reviewed because removing records can affect reported totals.

Availability means ensuring authorized users can access the system and its information when needed. SQLite stores the database in a local file, while Python can regenerate the analysis and charts from the CSV files. The business should keep secure backups of the original data and database and test that backups can be restored. This project does not implement automated backups or a production recovery process.

Overall, the project demonstrates the CIA triad at a basic educational level. Further controls would be needed before the system could safely manage real customer or business information.

## 11. Key Business Insights for Thabo

The cleaned dataset contains 43 sales records from the original 71 records. This means the results describe the records that passed the cleaning rules, rather than every original transaction. The removed records may include genuine sales, so Thabo should review incomplete source records before making major purchasing or staffing decisions.

In the latest recorded revenue results, 5kg Maize Meal generated R801.00, the highest listed product revenue. Eggs (6 pack) generated R364.00, followed by Bar One Chocolate at R224.00 and Sugar 1kg at R220.50. These figures suggest that maize meal was an important revenue contributor in the cleaned dataset. Thabo could monitor its availability and compare its sales over a longer period before changing order quantities.

The analysis recorded 52 units sold in January 2026 and 44 in February 2026. This is a decrease of eight units between those two months, but two months of data are not enough to establish a lasting trend or explain why the difference occurred. The average quantity per sales record was 2.23.

The application also provides queries for best-selling products, payment methods, category revenue, and customer types. Thabo can use these reports to investigate purchasing patterns and transaction preferences. Before acting on the findings, he should verify ambiguous dates, check missing records, and confirm that duplicate product names represent different product IDs where applicable. Regularly updating the data and reviewing reports over a longer period would support more reliable business decisions.

## 12. Final Checks and Submission

Before submitting:

- Run `python main.py` and confirm that it completes without errors.
- Confirm that both PNG charts exist and open correctly.
- Confirm that `store.db` exists and contains the two tables.
- Include `PLAN.md`, this README, all Python modules, the database, and both charts in the submission.
- Create `SUBMISSION.txt` containing your full name, student number, and GitHub repository URL.
- Ensure your GitHub repository has at least eight meaningful commits and does not contain a virtual environment.
- Create the required ZIP file using the naming convention `Surname_Firstname_KM04-05_Project.zip`.

## 13. Final Validation

The application was tested by running `python main.py` from the `starter_code` directory. The test completed successfully, including password verification, data cleaning, database creation, SQL reporting, Python analysis, and chart generation.

The cleaning process retained 12 product records and 43 sales records. The system generated the `revenue_per_product.png` and `monthly_trend.png` charts. SQLite foreign-key enforcement is enabled for database connections to help prevent sales records from referencing products that do not exist.

The final ZIP package includes the source CSV files, Python modules, SQLite database, charts, project plan, and documentation. Before submission, the package should be checked against the LMS requirements and the student number in `SUBMISSION.txt` should be confirmed.
