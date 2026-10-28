from langgraph.graph import StateGraph, START, END

from app.graph.state import NexusState

from app.graph.nodes import (
    load_business_data_node,
    market_research_node,
    finance_research_node,
    customer_research_node,
    business_analysis_node,
    decision_node,
    report_node,
    route_decision,
)


def build_graph():

    graph = StateGraph(NexusState)

    # ========================================================
    # NODES
    # ========================================================

    graph.add_node(
        "load_data",
        load_business_data_node
    )

    graph.add_node(
        "market_research",
        market_research_node
    )

    graph.add_node(
        "finance_research",
        finance_research_node
    )

    graph.add_node(
        "customer_research",
        customer_research_node
    )

    graph.add_node(
        "business_analysis",
        business_analysis_node
    )

    graph.add_node(
        "decision",
        decision_node
    )

    graph.add_node(
        "report",
        report_node
    )

    # ========================================================
    # START → LOAD DATA
    # ========================================================

    graph.add_edge(
        START,
        "load_data"
    )

    # ========================================================
    # LOAD DATA → PARALLEL RESEARCH
    # ========================================================

    graph.add_edge(
        "load_data",
        "market_research"
    )

    graph.add_edge(
        "load_data",
        "finance_research"
    )

    graph.add_edge(
        "load_data",
        "customer_research"
    )

    # ========================================================
    # RESEARCH → BUSINESS ANALYSIS
    # ========================================================

    graph.add_edge(
        "market_research",
        "business_analysis"
    )

    graph.add_edge(
        "finance_research",
        "business_analysis"
    )

    graph.add_edge(
        "customer_research",
        "business_analysis"
    )

    # ========================================================
    # BUSINESS ANALYSIS → DECISION
    # ========================================================

    graph.add_edge(
        "business_analysis",
        "decision"
    )

    # ========================================================
    # DECISION ROUTING
    # ========================================================

    graph.add_conditional_edges(
        "decision",
        route_decision,
        {
            "research": "market_research",
            "report": "report",
        }
    )

    # ========================================================
    # REPORT → END
    # ========================================================

    graph.add_edge(
        "report",
        END
    )

    return graph.compile()