from app.graph.workflow import build_graph


def main():

    print("=" * 60)
    print("NEXUS AUTONOMOUS BUSINESS INTELLIGENCE")
    print("=" * 60)

    query = input(
        "\nEnter your business question:\n> "
    )

    graph = build_graph()

    initial_state = {
        "question": query,
        "query": query,
        "iteration": 0
    }

    print("\nNEXUS is analyzing your business query...\n")

    result = graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("FINAL NEXUS REPORT")
    print("=" * 60)

    print(result.get(
        "executive_report",
        "No executive report generated."
    ))


if __name__ == "__main__":
    main()