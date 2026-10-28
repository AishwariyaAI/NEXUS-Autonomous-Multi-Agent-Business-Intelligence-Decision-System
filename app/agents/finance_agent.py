from app.agents.llm import get_llm


def finance_agent(state):
    """
    Financial Intelligence Agent.

    Uses actual KPIs and analytics from the uploaded dataset.
    Does not fabricate financial metrics.
    """

    query = state.get("query", state.get("question", ""))

    kpis = state.get("kpis", {})
    monthly_sales = state.get("monthly_sales", {})
    top_products = state.get("top_products", {})
    top_countries = state.get("top_countries", {})

    prompt = f"""
You are the Financial Intelligence Agent in NEXUS.

Business question:
{query}

ACTUAL BUSINESS DATA:

KPIs:
{kpis}

Monthly revenue:
{monthly_sales}

Top products:
{top_products}

Top countries:
{top_countries}

STRICT RULES:

1. Do NOT invent financial statistics.
2. Do NOT invent gross margin, COGS, operating expenses,
   profit, cash flow, churn, or other metrics that are not
   explicitly present in the supplied data.
3. Only calculate values that can be mathematically derived
   from the supplied data.
4. Clearly distinguish:
   - FACT
   - DERIVED METRIC
   - HYPOTHESIS
5. If profitability cannot be calculated from the dataset,
   explicitly say so.
6. Never turn an assumption into a fact.

Analyze:

## Financial Summary

## Revenue Analysis

## Order Analysis

## Average Order Value

## Monthly Trend

## Product Revenue Concentration

## Geographic Revenue Concentration

## Financial Risks

## Recommended Financial Actions

## Data Limitations

For every important numerical claim, use the supplied data.
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "finance_analysis": response.content
    }