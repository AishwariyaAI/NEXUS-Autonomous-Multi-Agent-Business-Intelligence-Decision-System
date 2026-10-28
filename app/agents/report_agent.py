# ============================================================
# NEXUS EXECUTIVE REPORTER
# ============================================================

import re

from app.agents.llm import get_llm


def executive_report_agent(state):

    # ========================================================
    # INPUTS
    # ========================================================

    question = state.get(
        "question",
        state.get(
            "query",
            ""
        )
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

    decision = state.get(
        "decision",
        "NEED_MORE_RESEARCH"
    )

    decision_score = state.get(
        "decision_score",
        0
    )

    decision_reason = state.get(
        "decision_reason",
        ""
    )

    recommendations = state.get(
        "recommendations",
        []
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
    # FORMAT RECOMMENDATIONS
    # ========================================================

    recommendation_text = ""

    if isinstance(
        recommendations,
        list
    ):

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            if isinstance(
                recommendation,
                dict
            ):

                action = recommendation.get(
                    "action",
                    "No action specified"
                )

                reason = recommendation.get(
                    "reason",
                    "No reason provided"
                )

                priority = recommendation.get(
                    "priority",
                    "MEDIUM"
                )

                evidence_type = recommendation.get(
                    "evidence_type",
                    "Unknown"
                )

                recommendation_text += f"""
### Recommendation {index}

**Action:** {action}

**Reason:** {reason}

**Priority:** {priority}

**Evidence Type:** {evidence_type}

"""

            else:

                recommendation_text += f"""
### Recommendation {index}

{str(recommendation)}

"""


    if not recommendation_text:

        recommendation_text = """
No explicit recommendations were returned.
The available evidence should be investigated further.
"""


    # ========================================================
    # LLM
    # ========================================================

    llm = get_llm()


    # ========================================================
    # REPORT PROMPT
    # ========================================================

    prompt = f"""
You are the Executive Reporter for NEXUS,
an autonomous multi-agent business intelligence
and decision system.

Create a professional executive-level business report.

============================================================
BUSINESS QUESTION
============================================================

{question}

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
DECISION
============================================================

Decision:
{decision}

Decision Score:
{decision_score}/100

Decision Reason:
{decision_reason}

============================================================
RECOMMENDATIONS
============================================================

{recommendation_text}

============================================================
REPORT RULES
============================================================

Use only information supplied above.

Do NOT invent:

- churn rates
- conversion rates
- cart abandonment
- customer satisfaction
- profit margins
- marketing ROI
- expected revenue growth
- expected conversion growth

unless explicitly supplied.

Clearly distinguish:

1. Evidence-Based Findings
2. Derived Insights
3. Hypotheses

============================================================
REQUIRED REPORT STRUCTURE
============================================================

# NEXUS Executive Business Report

## Executive Summary

Provide a concise management-level summary.

## Business KPIs

Present the available KPIs.

## Key Findings

Cover:

- Market
- Finance
- Customer
- Business Analysis

## Evidence-Based Insights

Explain what the dataset actually proves.

## Risks

Identify measurable business risks.

## Opportunities

Identify evidence-supported opportunities.

## Recommended Actions

Present the recommendations generated by the
Decision Agent.

## Decision

State:

Decision:
{decision}

Decision Score:
{decision_score}/100

Explain why this decision was reached.

## Evidence vs Hypotheses

Clearly separate confirmed evidence from assumptions
or hypotheses.

## Executive Conclusion

Give a concise final conclusion for management.

============================================================
IMPORTANT
============================================================

Return ONLY the report.

Do not return JSON.

Do not wrap the report inside quotation marks.
"""


    # ========================================================
    # CALL LLM
    # ========================================================

    try:

        response = llm.invoke(
            prompt
        )

        if hasattr(
            response,
            "content"
        ):

            report = response.content

        else:

            report = str(
                response
            )

    except Exception as e:

        report = f"""
# NEXUS Executive Business Report

## Executive Summary

NEXUS completed the multi-agent business analysis.

## Business KPIs

| KPI | Value |
|---|---:|
| Total Revenue | £{total_revenue:,.2f} |
| Total Orders | {total_orders:,} |
| Customers | {total_customers:,} |
| Average Order Value | £{average_order_value:,.2f} |

## Decision

**{decision}**

Decision Score: **{decision_score}/100**

### Decision Reason

{decision_reason}

## Recommended Actions

{recommendation_text}

## Executive Conclusion

The available business evidence should be used to
prioritize the recommended actions while validating
any hypotheses with additional operational data.

---

**Reporter fallback activated:** {str(e)}
"""


    # ========================================================
    # CLEAN RESPONSE
    # ========================================================

    if report is None:

        report = ""

    report = str(
        report
    ).strip()


    # Remove accidental ```markdown fences

    report = re.sub(
        r"^```(?:markdown|md)?\s*",
        "",
        report,
        flags=re.IGNORECASE
    )

    report = re.sub(
        r"\s*```$",
        "",
        report
    )


    # ========================================================
    # FINAL RETURN
    # ========================================================

    return {
        "executive_report": report
    }