# ============================================================
# NEXUS MARKET INTELLIGENCE AGENT
# ============================================================

from app.agents.llm import get_llm


def _content(response):
    """
    Safely extract text from an LLM response.
    """
    if hasattr(response, "content"):
        return str(response.content)

    return str(response)


# ============================================================
# MARKET RESEARCH AGENT
# ============================================================

def market_research_agent(state):
    """
    Market Intelligence Agent.

    Uses ONLY the business data supplied in NexusState.

    The agent:
    - analyzes sales trends
    - analyzes product concentration
    - analyzes geographic concentration
    - identifies risks
    - identifies opportunities
    - clearly separates evidence from hypotheses
    """

    # --------------------------------------------------------
    # INPUTS
    # --------------------------------------------------------

    query = state.get(
        "query",
        state.get(
            "question",
            ""
        )
    )

    kpis = state.get(
        "kpis",
        {}
    )

    monthly_sales = state.get(
        "monthly_sales",
        {}
    )

    top_products = state.get(
        "top_products",
        {}
    )

    top_countries = state.get(
        "top_countries",
        {}
    )

    customer_concentration = state.get(
        "customer_concentration",
        {}
    )

    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are the Market Intelligence Agent inside NEXUS,
an autonomous multi-agent business intelligence system.

Your responsibility is to analyze the uploaded business
dataset and identify market-related business insights.

============================================================
BUSINESS QUESTION
============================================================

{query}

============================================================
BUSINESS KPIs
============================================================

{kpis}

============================================================
MONTHLY SALES
============================================================

{monthly_sales}

============================================================
TOP PRODUCTS
============================================================

{top_products}

============================================================
TOP COUNTRIES
============================================================

{top_countries}

============================================================
CUSTOMER CONCENTRATION
============================================================

{customer_concentration}

============================================================
STRICT EVIDENCE RULES
============================================================

Use ONLY the supplied data.

DO NOT invent:

- competitor market share
- competitor pricing
- industry growth rates
- market size
- customer demographics
- conversion rates
- churn rates
- marketing performance
- cart abandonment
- profit margins

unless those values are explicitly supplied.

You MAY provide business hypotheses, but clearly label them
as:

Hypothesis
or
Assumption

If the dataset does not contain enough information to prove
something, explicitly say:

"The uploaded dataset does not provide enough evidence to
confirm this."

============================================================
ANALYSIS REQUIRED
============================================================

Analyze:

1. Revenue trends

2. Monthly sales patterns

3. Product concentration

4. Geographic concentration

5. Customer concentration if available

6. Market-related risks

7. Market-related opportunities

8. Possible causes of the business problem

9. Data gaps that prevent stronger conclusions

============================================================
REQUIRED OUTPUT
============================================================

Return ONLY the following structured analysis:

## Market Findings

Explain the most important market-related findings.

## Evidence From Uploaded Dataset

List concrete findings supported by the supplied metrics.

## Possible Causes

Separate confirmed evidence from hypotheses.

## Opportunities

Identify evidence-supported business opportunities.

## Risks

Identify measurable or clearly supported risks.

## Data Gaps

Explain what additional information would improve
the analysis.

Be concise but analytical.
"""

    # --------------------------------------------------------
    # CALL LLM
    # --------------------------------------------------------

    try:

        llm = get_llm()

        response = llm.invoke(
            prompt
        )

        analysis = _content(
            response
        )

    except Exception as e:

        analysis = (
            "## Market Findings\n\n"
            "Market Intelligence could not complete the "
            "LLM analysis.\n\n"
            f"Error: {str(e)}"
        )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        # Main state key used by LangGraph
        "market_analysis": analysis,

        # Optional structured agent information
        # useful for dashboard display/debugging
        "research_data": [
            {
                "agent": "market_research",
                "result": analysis
            }
        ]
    }