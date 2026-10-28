from app.agents.llm import get_llm


def business_analysis_agent(state):
    """
    Business Analyst Agent.

    Synthesizes Market, Finance and Customer intelligence
    while preserving the distinction between facts and hypotheses.
    """

    question = state.get("question", state.get("query", ""))

    kpis = state.get("kpis", {})
    monthly_sales = state.get("monthly_sales", {})
    top_products = state.get("top_products", {})
    top_countries = state.get("top_countries", {})

    market_analysis = state.get(
        "market_analysis",
        state.get("research_data", "Not available")
    )

    finance_analysis = state.get(
        "finance_analysis",
        "Not available"
    )

    customer_analysis = state.get(
        "customer_analysis",
        "Not available"
    )

    prompt = f"""
You are the Senior Business Analyst in NEXUS.

Business Question:
{question}

==================================================
ACTUAL DATA
==================================================

KPIs:
{kpis}

Monthly Sales:
{monthly_sales}

Top Products:
{top_products}

Top Countries:
{top_countries}

==================================================
AGENT INTELLIGENCE
==================================================

MARKET INTELLIGENCE:
{market_analysis}

FINANCIAL INTELLIGENCE:
{finance_analysis}

CUSTOMER INTELLIGENCE:
{customer_analysis}

==================================================
IMPORTANT RULES
==================================================

1. Treat the uploaded dataset as the source of truth.

2. Do NOT invent statistics.

3. Do NOT repeat unsupported claims from another agent
   as facts.

4. If an agent provides an unsupported number, ignore it.

5. Clearly separate:
   FACTS
   DERIVED METRICS
   HYPOTHESES
   RECOMMENDATIONS

6. Every numerical claim must either:
   - exist in the uploaded data, or
   - be mathematically derived from it.

7. Do not invent:
   - competitor market share
   - NPS
   - churn
   - gross margin
   - COGS
   - conversion rate
   - bounce rate
   - customer retention
   - industry averages
   unless supplied by the dataset.

==================================================
ANALYSIS
==================================================

Produce:

## Executive Diagnosis

Explain the most important business issue.

## Evidence-Based Findings

List findings directly supported by the dataset.

## Derived Insights

Calculate useful metrics where possible.

## Root Causes

Separate:

### Confirmed / Evidence-Based Causes
from

### Possible Causes / Hypotheses

## Business Impact

Discuss the likely business impact without inventing
unsupported financial numbers.

## Opportunities

Identify practical opportunities.

## Data Gaps

Explain what additional data would be required
to confirm uncertain causes.

Keep the analysis executive-friendly.
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "business_analysis": response.content
    }