# ============================================================
# NEXUS STATE
# ============================================================

from typing import TypedDict, Any


class NexusState(TypedDict, total=False):

    # ========================================================
    # USER INPUT
    # ========================================================

    question: str

    query: str

    # ========================================================
    # UPLOADED DATA
    # ========================================================

    uploaded_analytics: dict

    dataframe: Any

    raw_rows: int

    clean_rows: int

    columns: list

    # ========================================================
    # BUSINESS ANALYTICS
    # ========================================================

    kpis: dict

    monthly_sales: dict

    top_products: dict

    top_countries: dict

    customer_revenue: dict

    customer_concentration: dict

    # ========================================================
    # AGENT OUTPUTS
    # ========================================================

    market_analysis: str

    finance_analysis: str

    customer_analysis: str

    business_analysis: str

    research_data: list

    # ========================================================
    # DECISION
    # ========================================================

    decision: str

    decision_score: int

    decision_reason: str

    recommendations: list

    # ========================================================
    # FINAL REPORT
    # ========================================================

    executive_report: str

    # ========================================================
    # CONTROL
    # ========================================================

    iteration: int

    research_cycles: int