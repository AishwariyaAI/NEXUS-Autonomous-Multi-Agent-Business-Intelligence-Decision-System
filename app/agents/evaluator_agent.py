from app.agents.llm import get_llm


llm = get_llm()


def evaluator_agent(state):

    query = state["query"]

    analysis = state.get("analysis", {})
    recommendations = state.get("recommendations", [])

    analysis_text = analysis.get("summary", "")

    recommendations_text = "\n".join(
        str(item) for item in recommendations
    )

    prompt = f"""
You are the Decision Evaluation Agent inside NEXUS.

Business question:
{query}

Analysis:
{analysis_text[:4000]}

Recommendations:
{recommendations_text[:3000]}

Evaluate whether NEXUS has enough evidence
to make a reliable business decision.

Score the decision from 0 to 100.

Consider:

1. Evidence quality
2. Analysis completeness
3. Recommendation quality
4. Business risk
5. Missing information

Return ONLY this format:

SCORE: <number>
STATUS: APPROVE or RESEARCH
REASON: <short explanation>
"""

    response = llm.invoke(prompt)

    text = response.content.strip()

    score = 0

    for line in text.splitlines():
        if line.startswith("SCORE:"):
            try:
                score = float(
                    line.replace("SCORE:", "").strip()
                )
            except ValueError:
                score = 0

    status = "RESEARCH"

    if score >= 70:
        status = "APPROVE"

    return {
        "decision_score": score,
        "decision_status": status
    }