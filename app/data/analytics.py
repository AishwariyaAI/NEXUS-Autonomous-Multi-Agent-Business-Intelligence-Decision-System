import pandas as pd


# ============================================================
# DATA PREPARATION
# ============================================================

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare uploaded business data.

    Supports the Online Retail dataset and similar
    CSV/Excel business datasets.
    """

    df = df.copy()

    # --------------------------------------------------------
    # Normalize column names
    # --------------------------------------------------------

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    # --------------------------------------------------------
    # Remove completely empty rows
    # --------------------------------------------------------

    df = df.dropna(how="all")

    # --------------------------------------------------------
    # Detect important columns
    # --------------------------------------------------------

    column_map = {
        col.lower().replace(" ", "").replace("_", ""): col
        for col in df.columns
    }

    # Quantity
    quantity_col = None

    for key in [
        "quantity",
        "qty",
        "units",
        "unitsold",
    ]:
        if key in column_map:
            quantity_col = column_map[key]
            break

    # Unit price
    price_col = None

    for key in [
        "unitprice",
        "price",
        "unit_price",
        "salesprice",
    ]:
        normalized = key.lower().replace("_", "")

        if normalized in column_map:
            price_col = column_map[normalized]
            break

    # Revenue
    revenue_col = None

    for key in [
        "revenue",
        "sales",
        "sale",
        "salesamount",
        "totalrevenue",
        "total_sales",
        "amount",
        "turnover",
    ]:
        normalized = key.lower().replace("_", "")

        if normalized in column_map:
            revenue_col = column_map[normalized]
            break

    # --------------------------------------------------------
    # Calculate revenue if necessary
    # --------------------------------------------------------

    if revenue_col is None:

        if quantity_col is not None and price_col is not None:

            df[quantity_col] = pd.to_numeric(
                df[quantity_col],
                errors="coerce"
            )

            df[price_col] = pd.to_numeric(
                df[price_col],
                errors="coerce"
            )

            df["Revenue"] = (
                df[quantity_col] *
                df[price_col]
            )

            revenue_col = "Revenue"

        else:
            raise ValueError(
                "Unable to detect revenue or "
                "quantity + price columns."
            )

    else:

        df[revenue_col] = pd.to_numeric(
            df[revenue_col],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Remove invalid revenue
    # --------------------------------------------------------

    df = df.dropna(
        subset=[revenue_col]
    )

    # --------------------------------------------------------
    # Keep positive revenue transactions
    # --------------------------------------------------------

    df = df[df[revenue_col] > 0].copy()

    # --------------------------------------------------------
    # Standardize Revenue column
    # --------------------------------------------------------

    if revenue_col != "Revenue":

        df["Revenue"] = df[revenue_col]

    # --------------------------------------------------------
    # Detect CustomerID
    # --------------------------------------------------------

    customer_col = None

    for key in [
        "customerid",
        "customer_id",
        "customer",
        "customername",
        "clientid",
    ]:

        normalized = (
            key.lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if normalized in column_map:

            customer_col = column_map[normalized]
            break

    # --------------------------------------------------------
    # Detect invoice/order column
    # --------------------------------------------------------

    invoice_col = None

    for key in [
        "invoiceno",
        "invoice",
        "invoice_no",
        "orderno",
        "orderid",
        "order_id",
    ]:

        normalized = (
            key.lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if normalized in column_map:

            invoice_col = column_map[normalized]
            break

    # --------------------------------------------------------
    # Detect date column
    # --------------------------------------------------------

    date_col = None

    for key in [
        "invoicedate",
        "date",
        "orderdate",
        "transactiondate",
        "transaction_date",
    ]:

        normalized = (
            key.lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if normalized in column_map:

            date_col = column_map[normalized]
            break

    if date_col is not None:

        df[date_col] = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

    return df


# ============================================================
# BASIC KPIs
# ============================================================

def calculate_kpis(df: pd.DataFrame) -> dict:

    total_revenue = float(
        df["Revenue"].sum()
    )

    # --------------------------------------------------------
    # Orders
    # --------------------------------------------------------

    invoice_col = None

    for col in df.columns:

        normalized = (
            str(col)
            .lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if normalized in [
            "invoiceno",
            "invoice",
            "orderno",
            "orderid",
        ]:

            invoice_col = col
            break

    if invoice_col:

        total_orders = int(
            df[invoice_col]
            .nunique()
        )

    else:

        total_orders = int(
            len(df)
        )

    # --------------------------------------------------------
    # Customers
    # --------------------------------------------------------

    customer_col = None

    for col in df.columns:

        normalized = (
            str(col)
            .lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if normalized in [
            "customerid",
            "customer",
            "customername",
            "clientid",
        ]:

            customer_col = col
            break

    if customer_col:

        total_customers = int(
            df[customer_col]
            .nunique()
        )

    else:

        total_customers = 0

    # --------------------------------------------------------
    # AOV
    # --------------------------------------------------------

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    return {
        "total_revenue": round(
            total_revenue,
            2
        ),

        "total_orders": total_orders,

        "total_customers": total_customers,

        "average_order_value": round(
            average_order_value,
            2
        ),
    }


# ============================================================
# MONTHLY SALES
# ============================================================

def monthly_sales(df: pd.DataFrame):

    date_col = None

    for col in df.columns:

        normalized = (
            str(col)
            .lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if normalized in [
            "invoicedate",
            "date",
            "orderdate",
            "transactiondate",
        ]:

            date_col = col
            break

    if date_col is None:

        return {}

    temp = df.copy()

    temp[date_col] = pd.to_datetime(
        temp[date_col],
        errors="coerce"
    )

    temp = temp.dropna(
        subset=[date_col]
    )

    result = (
        temp
        .groupby(
            temp[date_col].dt.to_period("M")
        )["Revenue"]
        .sum()
        .sort_index()
    )

    return {
        str(index): round(
            float(value),
            2
        )
        for index, value in result.items()
    }


# ============================================================
# TOP PRODUCTS
# ============================================================

def top_products(
    df: pd.DataFrame,
    limit: int = 10
):

    product_col = None

    for col in df.columns:

        normalized = (
            str(col)
            .lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if normalized in [
            "description",
            "product",
            "productname",
            "item",
            "itemname",
        ]:

            product_col = col
            break

    if product_col is None:

        return {}

    result = (
        df.groupby(product_col)["Revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(limit)
    )

    return {
        str(index): round(
            float(value),
            2
        )
        for index, value in result.items()
    }


# ============================================================
# TOP COUNTRIES
# ============================================================

def top_countries(
    df: pd.DataFrame,
    limit: int = 10
):

    country_col = None

    for col in df.columns:

        normalized = (
            str(col)
            .lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if normalized in [
            "country",
            "countries",
            "region",
            "market",
        ]:

            country_col = col
            break

    if country_col is None:

        return {}

    result = (
        df.groupby(country_col)["Revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(limit)
    )

    return {
        str(index): round(
            float(value),
            2
        )
        for index, value in result.items()
    }


# ============================================================
# CUSTOMER REVENUE
# ============================================================

def customer_revenue(
    df: pd.DataFrame,
    limit: int = 20
):

    customer_col = None

    for col in df.columns:

        normalized = (
            str(col)
            .lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if normalized in [
            "customerid",
            "customer",
            "customername",
            "clientid",
        ]:

            customer_col = col
            break

    if customer_col is None:

        return {}

    result = (
        df.groupby(customer_col)["Revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(limit)
    )

    return {
        str(index): round(
            float(value),
            2
        )
        for index, value in result.items()
    }


# ============================================================
# CUSTOMER CONCENTRATION
# ============================================================

def customer_concentration(
    df: pd.DataFrame
) -> dict:
    """
    Calculate actual customer revenue concentration.

    This prevents the LLM from guessing whether the business
    follows a Pareto / 80-20 pattern.
    """

    customer_col = None

    for col in df.columns:

        normalized = (
            str(col)
            .lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if normalized in [
            "customerid",
            "customer",
            "customername",
            "clientid",
        ]:

            customer_col = col
            break

    # --------------------------------------------------------
    # Customer ID unavailable
    # --------------------------------------------------------

    if customer_col is None:

        return {
            "available": False,
            "reason": (
                "Customer-level identifier "
                "was not detected."
            )
        }

    # --------------------------------------------------------
    # Revenue by customer
    # --------------------------------------------------------

    customer_sales = (
        df.groupby(customer_col)["Revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    if customer_sales.empty:

        return {
            "available": False,
            "reason": "No customer revenue data available."
        }

    total_revenue = float(
        customer_sales.sum()
    )

    total_customers = int(
        customer_sales.shape[0]
    )

    # --------------------------------------------------------
    # Top 10 customers
    # --------------------------------------------------------

    top_10_revenue = float(
        customer_sales.head(10).sum()
    )

    top_10_percentage = (
        top_10_revenue /
        total_revenue *
        100
        if total_revenue > 0
        else 0
    )

    # --------------------------------------------------------
    # Top 20 customers
    # --------------------------------------------------------

    top_20_revenue = float(
        customer_sales.head(20).sum()
    )

    top_20_percentage = (
        top_20_revenue /
        total_revenue *
        100
        if total_revenue > 0
        else 0
    )

    # --------------------------------------------------------
    # Top 10% customers
    # --------------------------------------------------------

    top_10_percent_count = max(
        1,
        int(
            total_customers * 0.10
        )
    )

    top_10_percent_revenue = float(
        customer_sales
        .head(top_10_percent_count)
        .sum()
    )

    top_10_percent_share = (
        top_10_percent_revenue /
        total_revenue *
        100
        if total_revenue > 0
        else 0
    )

    # --------------------------------------------------------
    # Average revenue per customer
    # --------------------------------------------------------

    average_revenue_per_customer = (
        total_revenue /
        total_customers
        if total_customers > 0
        else 0
    )

    # --------------------------------------------------------
    # Concentration classification
    # --------------------------------------------------------

    if top_10_percent_share >= 70:

        concentration_level = "HIGH"

    elif top_10_percent_share >= 40:

        concentration_level = "MEDIUM"

    else:

        concentration_level = "LOW"

    return {

        "available": True,

        "total_customers": total_customers,

        "total_revenue": round(
            total_revenue,
            2
        ),

        "average_revenue_per_customer": round(
            average_revenue_per_customer,
            2
        ),

        "top_10_customers_revenue": round(
            top_10_revenue,
            2
        ),

        "top_10_customers_percentage": round(
            top_10_percentage,
            2
        ),

        "top_20_customers_revenue": round(
            top_20_revenue,
            2
        ),

        "top_20_customers_percentage": round(
            top_20_percentage,
            2
        ),

        "top_10_percent_customer_share": round(
            top_10_percent_share,
            2
        ),

        "concentration_level": concentration_level,
    }