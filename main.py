"""
Web Research Agent - Simple Example
===================================
Demonstrates how to use the SimpleResearchAgent (no AI required).
"""

from src.simple_research_agent import SimpleResearchAgent


def main():
    """Run simple research agent examples."""

    print("=" * 60)
    print("SIMPLE WEB RESEARCH AGENT")
    print("Uses Google Search + Web Scraping (No AI)")
    print("=" * 60)

    # Create the agent
    agent = SimpleResearchAgent()

    # Example 1: Quick search (just Google snippets)
    print("\n\nEXAMPLE 1: Quick Search")
    print("-" * 60)
    result = agent.quick_search("What is Python programming language")
    print(result)

    # Example 2: Full research (fetches and reads webpages)
    print("\n\nEXAMPLE 2: Full Research")
    print("-" * 60)
    research_result = agent.research(
        question="What is Python used for?",
        num_sources=2  # Check 2 websites
    )

    print("\n" + research_result['summary'])

    # Example 3: Check agent history
    print("\n\nEXAMPLE 3: Agent History")
    print("-" * 60)
    print(f"Agent performed {len(agent.get_history())} actions")
    for i, action in enumerate(agent.get_history(), 1):
        print(f"{i}. Used tool: {action['tool']}")


if __name__ == "__main__":
    main()
