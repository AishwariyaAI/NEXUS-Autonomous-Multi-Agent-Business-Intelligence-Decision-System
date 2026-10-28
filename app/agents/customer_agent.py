# ============================================================
# NEXUS CUSTOMER INTELLIGENCE AGENT
# ============================================================

from app.agents.llm import get_llm


# ============================================================
# CUSTOMER RESEARCH AGENT
# ============================================================

def customer_research_agent(state):

    # --------------------------------------------------------
    # Extract business information
    # --------------------------------------------------------

    kpis = state.get(
        "kpis",
        {}
    )

    customer_revenue = state.get(
        "customer_revenue",
        {}
    )

    customer_concentration = state.get(
        "customer_concentration",
        {}
    )

    query = state.get(
        "query",
        state.get(
            "question",
            ""
        )
    )

    # --------------------------------------------------------
    # Important KPI values
    # --------------------------------------------------------

    total_revenue = kpis.get(
        "total_revenue",
        0
    )

    total_orders = kpis.get(
        "total_orders",
        0
    )

    total_customers = kpis.get(
        "total_customers",
        0
    )

    average_order_value = kpis.get(
        "average_order_value",
        0
    )

    # --------------------------------------------------------
    # Customer concentration values
    # --------------------------------------------------------

    concentration_available = (
        customer_concentration.get(
            "available",
            False
        )
    )

    top_10_share = (
        customer_concentration.get(
            "top_10_customers_percentage",
            0
        )
    )

    top_20_share = (
        customer_concentration.get(
            "top_20_customers_percentage",
            0
        )
    )

    top_10_percent_share = (
        customer_concentration.get(
            "top_10_percent_customer_share",
            0
        )
    )

    concentration_level = (
        customer_concentration.get(
            "concentration_level",
            "UNKNOWN"
        )
    )

    avg_revenue_customer = (
        customer_concentration.get(
            "average_revenue_per_customer",
            0
        )
    )

    # --------------------------------------------------------
    # LLM
    # --------------------------------------------------------

    llm = get_llm()

    # --------------------------------------------------------
    # Customer Intelligence Prompt
    # --------------------------------------------------------

    prompt = f"""
You are the Customer Intelligence Agent inside NEXUS,
an autonomous multi-agent business intelligence system.

Your responsibility is to analyze customer behavior using
ONLY the supplied business data.

============================================================
BUSINESS QUERY
============================================================

{query}

============================================================
CUSTOMER KPIs
============================================================

Total Revenue:
{total_revenue}

Total Orders:
{total_orders}

Total Customers:
{total_customers}

Average Order Value:
{average_order_value}

Average Revenue Per Customer:
{avg_revenue_customer}

============================================================
CUSTOMER REVENUE
============================================================

{customer_revenue}

============================================================
CUSTOMER CONCENTRATION
============================================================

Customer-level concentration available:
{concentration_available}

Top 10 Customers Revenue Share:
{top_10_share}%

Top 20 Customers Revenue Share:
{top_20_share}%

Top 10% Customers Revenue Share:
{top_10_percent_share}%

Concentration Level:
{concentration_level}

============================================================
YOUR TASK
============================================================

Analyze:

1. Customer purchasing behavior

2. Customer revenue distribution

3. Customer concentration risk

4. Revenue dependency on high-value customers

5. Potential retention risks

6. Customer growth opportunities

7. Possible customer-related causes of business problems

8. Recommended customer strategies

============================================================
STRICT EVIDENCE RULE
============================================================

Use ONLY the supplied metrics.

DO NOT invent:

- churn rates
- retention rates
- customer satisfaction scores
- customer demographics
- customer acquisition costs
- customer lifetime value
- conversion rates

unless they are explicitly provided.

DO NOT claim that the company follows an
"80/20 rule" or "Pareto distribution" unless the
calculated customer concentration metrics support it.

DO NOT say:

"most revenue comes from a few customers"

unless the actual concentration metrics demonstrate this.

============================================================
OUTPUT FORMAT
============================================================

Return a structured analysis:

## Customer Overview

## Customer Revenue Distribution

## Customer Concentration

## Customer Risks

## Customer Opportunities

## Recommended Actions

## Evidence-Based Conclusion

Every important conclusion should reference
the supplied metrics where possible.
"""

    # --------------------------------------------------------
    # Call LLM
    # --------------------------------------------------------

    response = llm.invoke(
        prompt
    )

    # --------------------------------------------------------
    # Extract response
    # --------------------------------------------------------

    if hasattr(
        response,
        "content"
    ):

        analysis = response.content

    else:

        analysis = str(
            response
        )

    # --------------------------------------------------------
    # Return to LangGraph
    # --------------------------------------------------------

    return {

        "customer_analysis":
            analysis,

        "customer_concentration":
            customer_concentration,
    }