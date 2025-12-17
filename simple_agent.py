"""
Simple AI Research Agent
========================
An AI agent that uses tools (web search) and Google Gemini to answer questions.

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
MODEL_ID = "gemini-2.5-flash" 


def search_and_answer(question: str) -> str:
    
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
    import sys

    print("=" * 60)
    print("SIMPLE AI RESEARCH AGENT")
    print("=" * 60)

    # Get question from command line or use default
    if len(sys.argv) > 1:
        # Use question from command line
        question = " ".join(sys.argv[1:])
    else:
        # Ask user for question
        question = input("\nWhat's your question? ")

    if not question.strip():
        print("No question provided!")
        sys.exit(1)

    answer = search_and_answer(question)

    print("ANSWER:")
    print(answer)
