"""
Simple AI Research Agent
========================
An AI agent that uses tools (web search) and Google Gemini to answer questions.

Assignment Requirements:
✅ Uses a framework (Google Gemini AI)
✅ Uses tools (web search)
✅ Answers questions via LLM
"""

import os
from dotenv import load_dotenv
from google import genai
from src import tools

# Load API key from .env file
load_dotenv()

# Configure Google AI
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("Please add GOOGLE_API_KEY to .env file")

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-2.5-flash"  # Latest Gemini model


def search_and_answer(question: str) -> str:
    """
    AI agent that searches the web and answers questions.

    How it works:
    1. Tool: Search the web for information
    2. LLM: Use Google Gemini to analyze and answer

    Args:
        question: The question to answer

    Returns:
        AI-generated answer
    """
    print(f"\n[SEARCH] Searching for: {question}")

    # TOOL: Search the web
    search_results = tools.search_web(question, num_results=3)

    # Prepare context from search results
    context = "\n".join([
        f"{i+1}. {result['title']}\n   {result['snippet']}"
        for i, result in enumerate(search_results)
    ])

    print(f"[FOUND] {len(search_results)} sources")
    print(f"\n[AI] Generating answer...\n")

    # LLM: Generate answer using Google Gemini
    prompt = f"""Answer this question using the search results below:

QUESTION: {question}

SEARCH RESULTS:
{context}

Provide a clear, accurate answer based on these sources."""

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}\n\nSearch results were found, but AI couldn't process them."


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("SIMPLE AI RESEARCH AGENT")
    print("=" * 60)

    # Ask a question
    question = "What is Python used for?"
    answer = search_and_answer(question)

    print("ANSWER:")
    print(answer)
