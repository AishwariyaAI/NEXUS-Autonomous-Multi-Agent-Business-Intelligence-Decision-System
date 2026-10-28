# ============================================================
# NEXUS LLM CONFIGURATION
# ============================================================

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Load .env
load_dotenv(override=True)


# ============================================================
# GET LLM
# ============================================================

def get_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Check your .env file."
        )

    return ChatGroq(
        model="qwen/qwen3.6-27b",
        temperature=0.2,
        max_tokens=300,
        api_key=api_key
    )