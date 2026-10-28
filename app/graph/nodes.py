# ============================================================
# NEXUS LANGGRAPH NODES
# ============================================================

from typing import Dict, Any

from app.graph.state import NexusState
from app.data.loader import get_business_analytics

from app.agents.research_agents import market_research_agent
from app.agents.finance_agent import finance_agent
from app.agents.customer_agent import customer_research_agent
from app.agents.analysis_agent import business_analysis_agent
from app.agents.decision_agent import decision_agent
from app.agents.report_agent import executive_report_agent


# ============================================================
# HELPERS
# ============================================================

def _content(value):

    if hasattr(
        value,
        "content"
    ):
        return str(
            value.content
        )

    return str(
        value
    )


# ============================================================
# LOAD BUSINESS DATA
# ============================================================

def load_business_data_node(
    state: NexusState
) -> Dict[str, Any]:

    print(
        "Loading NEXUS business dataset..."
    )

    # --------------------------------------------------------
    # Uploaded dataset
    # --------------------------------------------------------

    uploaded_analytics = state.get(
        "uploaded_analytics"
    )

    if uploaded_analytics:

        analytics = uploaded_analytics

    else:

        # ----------------------------------------------------
        # Default dataset
        # ----------------------------------------------------

        analytics = get_business_analytics()

    # --------------------------------------------------------
    # Return analytics into LangGraph state
    # --------------------------------------------------------

    return {

        "kpis": analytics.get(
            "kpis",
            {}
        ),

        "monthly_sales": analytics.get(
            "monthly_sales",
            {}
        ),

        "top_products": analytics.get(
            "top_products",
            {}
        ),

        "top_countries": analytics.get(
            "top_countries",
            {}
        ),

        "customer_revenue": analytics.get(
            "customer_revenue",
            {}
        ),

        "customer_concentration": analytics.get(
            "customer_concentration",
            {}
        ),

        "raw_rows": analytics.get(
            "raw_rows",
            0
        ),

        "clean_rows": analytics.get(
            "clean_rows",
            0
        ),

        "columns": analytics.get(
            "columns",
            []
        )
    }


# ============================================================
# MARKET RESEARCH
# ============================================================

def market_research_node(
    state: NexusState
):

    result = market_research_agent(
        state
    )

    if isinstance(
        result,
        dict
    ):

        analysis = result.get(
            "market_analysis",
            ""
        )

        # Backward compatibility
        if not analysis:

            research_data = result.get(
                "research_data",
                []
            )

            if research_data:

                first = research_data[0]

                if isinstance(
                    first,
                    dict
                ):

                    analysis = first.get(
                        "result",
                        ""
                    )

        return {

            "market_analysis": analysis

        }

    return {

        "market_analysis": _content(
            result
        )

    }


# ============================================================
# FINANCE RESEARCH
# ============================================================

def finance_research_node(
    state: NexusState
):

    result = finance_agent(
        state
    )

    if isinstance(
        result,
        dict
    ):

        return {

            "finance_analysis": result.get(
                "finance_analysis",
                result.get(
                    "analysis",
                    ""
                )
            )

        }

    return {

        "finance_analysis": _content(
            result
        )

    }


# ============================================================
# CUSTOMER RESEARCH
# ============================================================

def customer_research_node(
    state: NexusState
):

    result = customer_research_agent(
        state
    )

    if isinstance(
        result,
        dict
    ):

        return {

            "customer_analysis": result.get(
                "customer_analysis",
                ""
            ),

            "customer_concentration": result.get(
                "customer_concentration",
                state.get(
                    "customer_concentration",
                    {}
                )
            )

        }

    return {

        "customer_analysis": _content(
            result
        )

    }


# ============================================================
# BUSINESS ANALYST
# ============================================================

def business_analysis_node(
    state: NexusState
):

    result = business_analysis_agent(
        state
    )

    if isinstance(
        result,
        dict
    ):

        return {

            "business_analysis": result.get(
                "business_analysis",
                result.get(
                    "analysis",
                    ""
                )
            )

        }

    return {

        "business_analysis": _content(
            result
        )

    }


# ============================================================
# DECISION AGENT
# ============================================================

def decision_node(
    state: NexusState
):

    result = decision_agent(
        state
    )

    if not isinstance(
        result,
        dict
    ):

        return {

            "decision": "NEED_MORE_RESEARCH",

            "decision_score": 0,

            "decision_reason": _content(
                result
            ),

            "recommendations": []

        }

    return {

        "decision": result.get(
            "decision",
            "NEED_MORE_RESEARCH"
        ),

        "decision_score": result.get(
            "decision_score",
            0
        ),

        "decision_reason": result.get(
            "decision_reason",
            ""
        ),

        "recommendations": result.get(
            "recommendations",
            []
        )

    }


# ============================================================
# DECISION ROUTER
# ============================================================

def route_decision(
    state: NexusState
):

    decision = str(
        state.get(
            "decision",
            "NEED_MORE_RESEARCH"
        )
    ).upper()

    iteration = int(
        state.get(
            "iteration",
            0
        )
    )

    # --------------------------------------------------------
    # Prevent infinite research loops
    # --------------------------------------------------------

    if iteration >= 1:

        return "report"

    # --------------------------------------------------------
    # Research required
    # --------------------------------------------------------

    if decision in {

        "RESEARCH",

        "RETRY",

        "INSUFFICIENT",

        "NEED_MORE_RESEARCH"

    }:

        return "research"

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    return "report"


# ============================================================
# EXECUTIVE REPORT
# ============================================================

def report_node(
    state: NexusState
):

    try:

        result = executive_report_agent(
            state
        )

        # ----------------------------------------------------
        # Dictionary response
        # ----------------------------------------------------

        if isinstance(
            result,
            dict
        ):

            report = result.get(
                "executive_report",
                ""
            )

            # Backward compatibility
            if not report:

                report = result.get(
                    "report",
                    ""
                )

        else:

            report = _content(
                result
            )

        # ----------------------------------------------------
        # Empty response protection
        # ----------------------------------------------------

        if not report or not str(
            report
        ).strip():

            report = """
# NEXUS Executive Business Report

## Executive Summary

NEXUS completed the multi-agent business analysis,
but the Executive Reporter returned an empty response.

## Decision

The available evidence should be reviewed before making
a final management decision.

## Recommended Actions

Review the recommendations generated by the Decision Agent.

## Executive Conclusion

Additional validation may be required before taking
high-impact business actions.
"""

        return {

            "executive_report": str(
                report
            ).strip()

        }

    except Exception as e:

        return {

            "executive_report": (
                "# NEXUS Executive Business Report\n\n"
                "## Reporter Error\n\n"
                f"The Executive Reporter encountered an error:\n\n"
                f"`{str(e)}`"
            )

        }