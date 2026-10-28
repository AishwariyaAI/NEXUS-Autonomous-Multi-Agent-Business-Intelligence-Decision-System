from app.agents.llm import get_llm


llm = get_llm()


def critic_agent(
    question: str,
    analysis: str
) -> str:

    prompt = f"""
You are a critical AI business reviewer.

Business question:
{question}

Current business analysis:
{analysis}

Your job is NOT to blindly agree with the analysis.

Check:

1. Unsupported claims
2. Missing evidence
3. Weak assumptions
4. Contradictions
5. Missing risks
6. Missing customer information
7. Missing competitor information

At the end classify the analysis as:

APPROVED

or

MORE_RESEARCH_REQUIRED

Then explain why.
"""

    response = llm.invoke(prompt)

    return response.content