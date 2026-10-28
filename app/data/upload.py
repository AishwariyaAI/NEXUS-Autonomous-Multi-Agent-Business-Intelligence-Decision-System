"""
NEXUS Dataset Upload & Processing
---------------------------------

Handles:
- CSV uploads
- Excel uploads
- Column detection
- Column normalization
- Revenue calculation
- Data cleaning
- Dataset validation
- Analytics generation
"""

import io
import re

import pandas as pd


# ============================================================
# COLUMN ALIASES
# ============================================================

COLUMN_ALIASES = {
    "revenue": [
        "revenue",
        "sales",
        "sale",
        "salesamount",
        "sales_amount",
        "total_sales",
        "totalsales",
        "total_revenue",
        "totalrevenue",
        "revenue_amount",
        "amount",
        "turnover",
        "income",
        "gmv",
    ],

    "quantity": [
        "quantity",
        "qty",
        "units",
        "unit_quantity",
        "units_sold",
        "volume",
    ],

    "price": [
        "unitprice",
        "unit_price",
        "price",
        "selling_price",
        "sellingprice",
        "item_price",
        "itemprice",
        "rate",
    ],

    "product": [
        "description",
        "product",
        "product_name",
        "productname",
        "item",
        "item_name",
        "itemname",
        "sku",
        "stockcode",
        "stock_code",
    ],

    "customer": [
        "customerid",
        "customer_id",
        "customer",
        "customer_name",
        "customername",
        "client",
        "client_id",
    ],

    "country": [
        "country",
        "region",
        "market",
        "location",
        "country_name",
    ],

    "date": [
        "invoicedate",
        "invoice_date",
        "date",
        "order_date",
        "orderdate",
        "transaction_date",
        "transactiondate",
        "created_at",
        "timestamp",
    ],

    "order": [
        "invoice",
        "invoice_no",
        "invoice_number",
        "order_id",
        "orderid",
        "transaction_id",
        "transactionid",
    ],
}


# ============================================================
# NORMALIZATION HELPERS
# ============================================================

def normalize_column_name(column):
    """
    Converts a column name into a comparable format.

    Example:
        "Unit Price" -> "unitprice"
        "Total Revenue" -> "totalrevenue"
    """

    column = str(column).strip().lower()

    column = re.sub(r"[^a-z0-9]+", "_", column)

    column = column.strip("_")

    return column


def find_column(df, aliases):
    """
    Finds the first matching dataframe column from aliases.
    """

    normalized_columns = {
        normalize_column_name(col): col
        for col in df.columns
    }

    for alias in aliases:

        normalized_alias = normalize_column_name(alias)

        if normalized_alias in normalized_columns:
            return normalized_columns[normalized_alias]

    # Fuzzy matching
    for normalized_name, original_name in normalized_columns.items():

        for alias in aliases:

            normalized_alias = normalize_column_name(alias)

            if (
                normalized_alias in normalized_name
                or normalized_name in normalized_alias
            ):
                return original_name

    return None


# ============================================================
# FILE READER
# ============================================================

def read_uploaded_file(uploaded_file):
    """
    Reads CSV or Excel files uploaded through Streamlit.
    """

    if uploaded_file is None:
        raise ValueError("No file was uploaded.")

    filename = getattr(uploaded_file, "name", "")

    filename = filename.lower()

    try:

        if filename.endswith(".csv"):

            return pd.read_csv(uploaded_file)

        if filename.endswith(".xlsx"):

            return pd.read_excel(uploaded_file)

        if filename.endswith(".xls"):

            return pd.read_excel(uploaded_file)

        raise ValueError(
            "Unsupported file format. Please upload CSV, XLS or XLSX."
        )

    except Exception as exc:

        raise ValueError(
            f"Unable to read uploaded file: {exc}"
        ) from exc


# ============================================================
# NORMALIZE DATAFRAME
# ============================================================

def normalize_dataframe(df):
    """
    Detects important business columns and creates
    standardized NEXUS columns where possible.
    """

    df = df.copy()

    # Keep original column names initially
    original_columns = list(df.columns)

    # Detect columns
    revenue_col = find_column(
        df,
        COLUMN_ALIASES["revenue"]
    )

    quantity_col = find_column(
        df,
        COLUMN_ALIASES["quantity"]
    )

    price_col = find_column(
        df,
        COLUMN_ALIASES["price"]
    )

    product_col = find_column(
        df,
        COLUMN_ALIASES["product"]
    )

    customer_col = find_column(
        df,
        COLUMN_ALIASES["customer"]
    )

    country_col = find_column(
        df,
        COLUMN_ALIASES["country"]
    )

    date_col = find_column(
        df,
        COLUMN_ALIASES["date"]
    )

    order_col = find_column(
        df,
        COLUMN_ALIASES["order"]
    )

    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    if revenue_col is not None:

        df["Revenue"] = pd.to_numeric(
            df[revenue_col],
            errors="coerce"
        )

    elif quantity_col is not None and price_col is not None:

        quantity = pd.to_numeric(
            df[quantity_col],
            errors="coerce"
        )

        price = pd.to_numeric(
            df[price_col],
            errors="coerce"
        )

        df["Revenue"] = quantity * price

    # --------------------------------------------------------
    # QUANTITY
    # --------------------------------------------------------

    if quantity_col is not None:

        df["Quantity"] = pd.to_numeric(
            df[quantity_col],
            errors="coerce"
        )

    # --------------------------------------------------------
    # UNIT PRICE
    # --------------------------------------------------------

    if price_col is not None:

        df["UnitPrice"] = pd.to_numeric(
            df[price_col],
            errors="coerce"
        )

    # --------------------------------------------------------
    # PRODUCT
    # --------------------------------------------------------

    if product_col is not None:

        df["Description"] = (
            df[product_col]
            .astype(str)
            .replace("nan", "")
        )

    # --------------------------------------------------------
    # CUSTOMER
    # --------------------------------------------------------

    if customer_col is not None:

        df["CustomerID"] = df[customer_col]

    # --------------------------------------------------------
    # COUNTRY
    # --------------------------------------------------------

    if country_col is not None:

        df["Country"] = (
            df[country_col]
            .astype(str)
            .replace("nan", "")
        )

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    if date_col is not None:

        df["InvoiceDate"] = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

    # --------------------------------------------------------
    # ORDER
    # --------------------------------------------------------

    if order_col is not None:

        df["Invoice"] = df[order_col]

    return df, {
        "revenue_column": revenue_col,
        "quantity_column": quantity_col,
        "price_column": price_col,
        "product_column": product_col,
        "customer_column": customer_col,
        "country_column": country_col,
        "date_column": date_col,
        "order_column": order_col,
        "original_columns": original_columns,
    }


# ============================================================
# CLEAN DATA
# ============================================================

def clean_uploaded_data(df):
    """
    Cleans uploaded business data.
    """

    df = df.copy()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Revenue must be numeric when available
    if "Revenue" in df.columns:

        df["Revenue"] = pd.to_numeric(
            df["Revenue"],
            errors="coerce"
        )

        # Remove rows where revenue is missing
        df = df.dropna(
            subset=["Revenue"]
        )

        # Keep positive business transactions
        df = df[df["Revenue"] >= 0]

    # Quantity
    if "Quantity" in df.columns:

        df["Quantity"] = pd.to_numeric(
            df["Quantity"],
            errors="coerce"
        )

    # Unit price
    if "UnitPrice" in df.columns:

        df["UnitPrice"] = pd.to_numeric(
            df["UnitPrice"],
            errors="coerce"
        )

    # Date
    if "InvoiceDate" in df.columns:

        df["InvoiceDate"] = pd.to_datetime(
            df["InvoiceDate"],
            errors="coerce"
        )

    return df.reset_index(drop=True)


# ============================================================
# VALIDATION
# ============================================================

def validate_dataset(
    df,
    raw_rows,
    clean_rows,
    detected_columns
):
    """
    Validates the uploaded business dataset.
    """

    errors = []
    warnings = []

    # Revenue validation
    has_revenue = "Revenue" in df.columns

    if not has_revenue:

        errors.append(
            "No revenue/price column was detected. "
            "Provide a revenue/sales column or both "
            "quantity and price columns."
        )

    elif df["Revenue"].notna().sum() == 0:

        errors.append(
            "Revenue column exists but contains no valid numeric values."
        )

    # Empty dataset
    if clean_rows == 0:

        errors.append(
            "Dataset contains no usable rows after cleaning."
        )

    # Small dataset warning
    if clean_rows > 0 and clean_rows < 10:

        warnings.append(
            "Dataset contains fewer than 10 usable rows."
        )

    # Missing optional fields
    if "InvoiceDate" not in df.columns:

        warnings.append(
            "No date column detected. Monthly revenue analysis "
            "may not be available."
        )

    if "CustomerID" not in df.columns:

        warnings.append(
            "No customer column detected. Customer analytics "
            "may be limited."
        )

    if "Description" not in df.columns:

        warnings.append(
            "No product/description column detected. "
            "Product analytics may be limited."
        )

    if "Country" not in df.columns:

        warnings.append(
            "No country/region column detected. "
            "Geographic analytics may be limited."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "raw_rows": int(raw_rows),
        "clean_rows": int(clean_rows),
        "detected_columns": detected_columns,
        "summary": {
            "raw_rows": int(raw_rows),
            "clean_rows": int(clean_rows),
            "columns": len(df.columns),
        },
    }


# ============================================================
# KPI CALCULATIONS
# ============================================================

def calculate_upload_kpis(df):
    """
    Calculates generic KPIs from uploaded data.
    """

    total_revenue = 0.0
    total_orders = 0
    total_customers = 0
    average_order_value = 0.0

    # Revenue
    if "Revenue" in df.columns:

        total_revenue = float(
            pd.to_numeric(
                df["Revenue"],
                errors="coerce"
            ).fillna(0).sum()
        )

    # Orders
    if "Invoice" in df.columns:

        total_orders = int(
            df["Invoice"].nunique()
        )

    else:

        total_orders = int(len(df))

    # Customers
    if "CustomerID" in df.columns:

        customers = df["CustomerID"].dropna()

        total_customers = int(
            customers.nunique()
        )

    # AOV
    if total_orders > 0:

        average_order_value = (
            total_revenue / total_orders
        )

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "average_order_value": average_order_value,
    }


# ============================================================
# GENERIC ANALYTICS
# ============================================================

def calculate_upload_analytics(df):
    """
    Calculates analytics that work with a wide range
    of business datasets.
    """

    analytics = {}

    # --------------------------------------------------------
    # MONTHLY SALES
    # --------------------------------------------------------

    if (
        "InvoiceDate" in df.columns
        and "Revenue" in df.columns
    ):

        temp = df.dropna(
            subset=["InvoiceDate"]
        ).copy()

        if not temp.empty:

            temp["Month"] = (
                temp["InvoiceDate"]
                .dt.to_period("M")
                .astype(str)
            )

            monthly = (
                temp.groupby("Month")["Revenue"]
                .sum()
                .reset_index()
            )

            monthly.columns = [
                "Month",
                "Revenue",
            ]

            analytics["monthly_sales"] = monthly

    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------

    if (
        "Description" in df.columns
        and "Revenue" in df.columns
    ):

        products = (
            df.groupby("Description")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        analytics["top_products"] = products

    # --------------------------------------------------------
    # TOP COUNTRIES
    # --------------------------------------------------------

    if (
        "Country" in df.columns
        and "Revenue" in df.columns
    ):

        countries = (
            df.groupby("Country")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        analytics["top_countries"] = countries

    # --------------------------------------------------------
    # CUSTOMER REVENUE
    # --------------------------------------------------------

    if (
        "CustomerID" in df.columns
        and "Revenue" in df.columns
    ):

        customer_revenue = (
            df.groupby("CustomerID")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(20)
            .reset_index()
        )

        analytics["customer_revenue"] = customer_revenue

    return analytics


# ============================================================
# MAIN DATASET PROCESSOR
# ============================================================

def process_uploaded_dataset(uploaded_file):
    """
    Complete NEXUS upload pipeline.

    Upload
        ↓
    Read CSV / Excel
        ↓
    Detect columns
        ↓
    Normalize columns
        ↓
    Calculate revenue
        ↓
    Clean data
        ↓
    Validate
        ↓
    Calculate analytics
    """

    # --------------------------------------------------------
    # READ FILE
    # --------------------------------------------------------

    df = read_uploaded_file(
        uploaded_file
    )

    raw_rows = len(df)

    # --------------------------------------------------------
    # NORMALIZE
    # --------------------------------------------------------

    df, detected_columns = normalize_dataframe(
        df
    )

    # --------------------------------------------------------
    # CLEAN
    # --------------------------------------------------------

    df = clean_uploaded_data(
        df
    )

    clean_rows = len(df)

    # --------------------------------------------------------
    # VALIDATE
    # --------------------------------------------------------

    validation = validate_dataset(
        df=df,
        raw_rows=raw_rows,
        clean_rows=clean_rows,
        detected_columns=detected_columns,
    )

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    kpis = calculate_upload_kpis(
        df
    )

    analytics = calculate_upload_analytics(
        df
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {
        "data": df,

        "validation": validation,

        # Important:
        # Keep these at the top level too.
        "raw_rows": raw_rows,
        "clean_rows": clean_rows,

        "kpis": kpis,

        "monthly_sales": analytics.get(
            "monthly_sales",
            pd.DataFrame()
        ),

        "top_products": analytics.get(
            "top_products",
            pd.DataFrame()
        ),

        "top_countries": analytics.get(
            "top_countries",
            pd.DataFrame()
        ),

        "customer_revenue": analytics.get(
            "customer_revenue",
            pd.DataFrame()
        ),

        "columns": list(df.columns),

        "success": validation["valid"],
    }


# ============================================================
# DASHBOARD PUBLIC FUNCTION
# ============================================================

def process_uploaded_file(uploaded_file):
    """
    Public function used by dashboard.py.

    Always returns a dictionary.
    """

    return process_uploaded_dataset(
        uploaded_file
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def process_uploaded_excel(uploaded_file):
    """
    Backward-compatible alias.
    """

    return process_uploaded_file(
        uploaded_file
    )


def process_upload(uploaded_file):
    """
    Backward-compatible alias.
    """

    return process_uploaded_file(
        uploaded_file
    )