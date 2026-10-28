from app.graph.workflow import build_graph


def main():

    print("=" * 60)
    print("        NEXUS AI")
    print("Autonomous Business Intelligence System")
    print("=" * 60)

    question = input(
        "\nEnter your business question:\n> "
    )

    graph = build_graph()

    initial_state = {
        "business_question": question,
        "research_iteration": 0,
        "market_data": [],
        "competitor_data": [],
        "customer_data": []
    }

    result = graph.invoke(initial_state)

    print("\n")
    print("=" * 60)
    print("              NEXUS RESULT")
    print("=" * 60)

    print(
        result.get(
            "final_report",
            "No final report generated."
        )
    )

    print("\n")
    print("Confidence:",
          result.get("confidence", 0))

    print(
        "Research iterations:",
        result.get("research_iteration", 0)
    )


if __name__ == "__main__":
    main()