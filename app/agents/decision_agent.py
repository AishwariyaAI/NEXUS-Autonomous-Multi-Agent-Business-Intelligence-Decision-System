# ============================================================
# NEXUS DECISION AGENT
# ============================================================

import json
import re

from app.agents.llm import get_llm


def decision_agent(state):

    # ========================================================
    # INPUT DATA
    # ========================================================

    query = state.get(
        "query",
        state.get("question", "")
    )

    kpis = state.get(
        "kpis",
        {}
    )

    market_analysis = state.get(
        "market_analysis",
        ""
    )

    finance_analysis = state.get(
        "finance_analysis",
        ""
    )

    customer_analysis = state.get(
        "customer_analysis",
        ""
    )

    business_analysis = state.get(
        "business_analysis",
        ""
    )

    customer_concentration = state.get(
        "customer_concentration",
        {}
    )


    # ========================================================
    # KPI VALUES
    # ========================================================

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


    # ========================================================
    # CUSTOMER CONCENTRATION
    # ========================================================

    concentration_level = customer_concentration.get(
        "concentration_level",
        "UNKNOWN"
    )

    top_10_percent_share = customer_concentration.get(
        "top_10_percent_customer_share",
        0
    )


    # ========================================================
    # LLM
    # ========================================================

    llm = get_llm()


    # ========================================================
    # DECISION PROMPT
    # ========================================================

    prompt = f"""
You are the Decision Agent inside NEXUS.

Your responsibility is to convert the evidence produced
by multiple business intelligence agents into:

1. A decision score
2. A decision
3. A reason
4. Evidence-based recommendations

============================================================
BUSINESS QUESTION
============================================================

{query}

============================================================
BUSINESS KPIs
============================================================

Total Revenue:
£{total_revenue:,.2f}

Total Orders:
{total_orders:,}

Total Customers:
{total_customers:,}

Average Order Value:
£{average_order_value:,.2f}

============================================================
CUSTOMER CONCENTRATION
============================================================

Concentration Level:
{concentration_level}

Top 10% Customer Revenue Share:
{top_10_percent_share:.2f}%

============================================================
MARKET INTELLIGENCE
============================================================

{market_analysis}

============================================================
FINANCIAL INTELLIGENCE
============================================================

{finance_analysis}

============================================================
CUSTOMER INTELLIGENCE
============================================================

{customer_analysis}

============================================================
BUSINESS ANALYSIS
============================================================

{business_analysis}

============================================================
EVIDENCE RULES
============================================================

Use ONLY information supplied above.

Never invent:

- conversion rates
- cart abandonment rates
- churn rates
- retention rates
- customer satisfaction scores
- mobile conversion rates
- marketing ROI
- profit margins
- expected revenue increases
- expected conversion increases

unless explicitly provided.

Every recommendation must be connected to
observable evidence.

============================================================
IMPORTANT DECISION RULE
============================================================

NEED_MORE_RESEARCH does NOT mean that there should be
zero recommendations.

If evidence is incomplete:

Decision:
NEED_MORE_RESEARCH

But still provide recommendations such as:

- investigate the missing metric
- diversify geographic dependency
- investigate customer concentration
- investigate seasonal demand
- prioritize high-performing products
- investigate underperforming products
- improve data collection

Recommendations must be useful and evidence-based.

============================================================
DECISION SCORE
============================================================

Calculate a score from 0 to 100.

Use:

80-100:
APPROVE

60-79:
APPROVE_WITH_CAUTION

40-59:
NEED_MORE_RESEARCH

0-39:
REJECT

============================================================
RECOMMENDATION RULE
============================================================

Return at least 3 recommendations.

Each recommendation must contain:

action
reason
priority
evidence_type

Evidence types:

Evidence-Based
Derived Insight
Hypothesis

============================================================
OUTPUT
============================================================

Return ONLY valid JSON.

Example:

{{
    "decision": "APPROVE_WITH_CAUTION",

    "decision_score": 72,

    "decision_reason":
        "The dataset provides strong revenue, order, product,
        geographic and customer evidence, but some operational
        metrics are unavailable.",

    "recommendations": [

        {{
            "action":
                "Diversify geographic revenue dependency",

            "reason":
                "The United Kingdom contributes approximately
                84% of total revenue.",

            "priority":
                "HIGH",

            "evidence_type":
                "Evidence-Based"
        }},

        {{
            "action":
                "Investigate customer concentration",

            "reason":
                "Customer-level revenue concentration should be
                evaluated before making retention decisions.",

            "priority":
                "MEDIUM",

            "evidence_type":
                "Derived Insight"
        }},

        {{
            "action":
                "Plan inventory and marketing around seasonal demand",

            "reason":
                "Monthly revenue shows significant variation across
                the observed period.",

            "priority":
                "MEDIUM",

            "evidence_type":
                "Evidence-Based"
        }}

    ]
}}

IMPORTANT:

Always return at least THREE recommendations.

Never return:

"recommendations": []

unless there is literally no business data.
"""


    # ========================================================
    # CALL LLM
    # ========================================================

    response = llm.invoke(
        prompt
    )


    if hasattr(
        response,
        "content"
    ):

        content = response.content

    else:

        content = str(
            response
        )


    # ========================================================
    # PARSE JSON
    # ========================================================

    try:

        match = re.search(
            r"\{.*\}",
            content,
            re.DOTALL
        )

        if not match:

            raise ValueError(
                "Decision Agent did not return JSON."
            )

        decision_data = json.loads(
            match.group()
        )

    except Exception:

        # ====================================================
        # SAFE FALLBACK
        # ====================================================

        decision_data = {

            "decision":
                "NEED_MORE_RESEARCH",

            "decision_score":
                50,

            "decision_reason":
                (
                    "The available dataset provides useful "
                    "business evidence, but additional data "
                    "is required for a high-confidence decision."
                ),

            "recommendations": [

                {
                    "action":
                        "Investigate geographic revenue concentration",

                    "reason":
                        (
                            "The uploaded dataset contains "
                            "country-level revenue information."
                        ),

                    "priority":
                        "HIGH",

                    "evidence_type":
                        "Evidence-Based"
                },

                {
                    "action":
                        "Investigate customer revenue concentration",

                    "reason":
                        (
                            "Customer-level revenue analysis "
                            "can identify dependency on high-value customers."
                        ),

                    "priority":
                        "MEDIUM",

                    "evidence_type":
                        "Derived Insight"
                },

                {
                    "action":
                        "Analyze seasonal sales patterns",

                    "reason":
                        (
                            "Monthly sales data can reveal "
                            "periods of unusually high or low demand."
                        ),

                    "priority":
                        "MEDIUM",

                    "evidence_type":
                        "Evidence-Based"
                }

            ]
        }


    # ========================================================
    # VALIDATE DECISION
    # ========================================================

    valid_decisions = {
        "APPROVE",
        "APPROVE_WITH_CAUTION",
        "NEED_MORE_RESEARCH",
        "REJECT"
    }

    decision = str(
        decision_data.get(
            "decision",
            "NEED_MORE_RESEARCH"
        )
    ).upper()


    if decision not in valid_decisions:

        decision = (
            "NEED_MORE_RESEARCH"
        )


    # ========================================================
    # VALIDATE SCORE
    # ========================================================

    try:

        score = int(
            decision_data.get(
                "decision_score",
                50
            )
        )

    except Exception:

        score = 50


    score = max(
        0,
        min(
            100,
            score
        )
    )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    recommendations = decision_data.get(
        "recommendations",
        []
    )


    if not isinstance(
        recommendations,
        list
    ):

        recommendations = []


    # ========================================================
    # GUARANTEE RECOMMENDATIONS
    # ========================================================

    if len(recommendations) == 0:

        recommendations = [

            {
                "action":
                    "Investigate geographic revenue concentration",

                "reason":
                    (
                        "Country-level revenue data is available "
                        "and should be evaluated for geographic risk."
                    ),

                "priority":
                    "HIGH",

                "evidence_type":
                    "Evidence-Based"
            },

            {
                "action":
                    "Analyze customer revenue concentration",

                "reason":
                    (
                        "Customer-level revenue information can "
                        "identify dependency on high-value customers."
                    ),

                "priority":
                    "MEDIUM",

                "evidence_type":
                    "Derived Insight"
            },

            {
                "action":
                    "Use monthly sales trends to plan inventory",

                "reason":
                    (
                        "Monthly revenue patterns can reveal "
                        "seasonality and demand fluctuations."
                    ),

                "priority":
                    "MEDIUM",

                "evidence_type":
                    "Evidence-Based"
            }

        ]


    # ========================================================
    # RETURN LANGGRAPH STATE
    # ========================================================

    return {

        "decision":
            decision,

        "decision_score":
            score,

        "decision_reason":
            decision_data.get(
                "decision_reason",
                "Decision generated from available evidence."
            ),

        "recommendations":
            recommendations
    }