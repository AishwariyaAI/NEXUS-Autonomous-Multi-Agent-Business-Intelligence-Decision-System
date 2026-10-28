import pandas as pd

from app.data.analytics import (
    prepare_data,
    calculate_kpis,
    monthly_sales,
    top_products,
    top_countries,
    customer_revenue,
    customer_concentration,
)


# ============================================================
# DEFAULT DATASET
# ============================================================

DATA_PATH = "data/Online Retail.xlsx"


# ============================================================
# LOAD BUSINESS DATA
# ============================================================

def load_business_data():

    print("Loading NEXUS business dataset...")

    df = pd.read_excel(DATA_PATH)

    print(f"Raw rows: {len(df):,}")

    df = prepare_data(df)

    print(f"Clean rows: {len(df):,}")

    return df


# ============================================================
# BUSINESS ANALYTICS
# ============================================================

def get_business_analytics():

    df = load_business_data()

    # --------------------------------------------------------
    # Calculate all analytics
    # --------------------------------------------------------

    analytics = {

        "data": df,

        "kpis": calculate_kpis(df),

        "monthly_sales": monthly_sales(df),

        "top_products": top_products(df),

        "top_countries": top_countries(df),

        "customer_revenue": customer_revenue(df),

        "customer_concentration": customer_concentration(df),
    }

    return analytics