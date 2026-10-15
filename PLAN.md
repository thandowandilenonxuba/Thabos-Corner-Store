# Thabo's Corner Store — Project Plan

## 1. Decomposition
I divided the project into smaller tasks: inspect the raw CSV files, clean the data, create an SQLite database, write SQL queries, analyse the data using Python, generate charts, implement password protection, and document the results.

## 2. Pattern Recognition
I expected to find missing product names and prices, inconsistent category capitalisation, duplicate records, invalid product references, missing quantities, and dates written in different formats. These problems could affect the accuracy of sales reports.

## 3. Abstraction
The system focuses on information useful to the store owner, such as product revenue, monthly sales trends, average basket size, and stock alerts. The original CSV files remain available as raw data.

## 4. Algorithm and Implementation Order
The workflow is to load the CSV files, clean the product and sales records, create and populate the relational database, execute SQL queries, calculate business insights using Python, generate charts, and protect access to reports with password verification. The final steps are to document the cleaning decisions and findings, test the complete application, commit the work to GitHub, and prepare the submission ZIP file.

## 5. Expected Outcome
The completed system should turn inconsistent spreadsheet data into organised database records and useful reports that help Thabo understand product performance and monthly sales trends.

## 6. Inputs, Processing, and Outputs

### Inputs
The system uses `Products.csv` and `Sales.csv` as its source files. The product file contains product details, while the sales file contains transaction details.

### Processing
Python and pandas load and clean the records by handling missing values, duplicates, inconsistent categories, date formats, and invalid product references. The cleaned records are stored in related SQLite tables. SQL queries and Python functions calculate sales revenue, product performance, monthly trends, average basket size, and low-stock alerts. Password verification controls access to the reports.

### Outputs
The system produces a SQLite database named `store.db`, SQL query results, a revenue-per-product bar chart, a monthly sales trend line chart, and business insights documented in the README file.

### Validation
The application is tested by running `python main.py`. The test checks that authentication, data cleaning, database operations, analysis, and chart generation complete without errors.