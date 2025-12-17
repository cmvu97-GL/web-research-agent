"""
Simple Research Agent
====================
A basic web research agent that uses Google search and webpage scraping.
No AI required - uses simple rule-based logic.
"""

from typing import Dict, List
from .base_agent import BaseAgent
from . import tools


class SimpleResearchAgent(BaseAgent):
    """
    A simple research agent without AI.

    HOW IT WORKS:
    1. Search Google for the question
    2. Fetch the top result
    3. Extract and return the text

    LIMITATIONS (without AI):
    - Can't understand context
    - Can't synthesize from multiple sources
    - Just returns raw information

    BENEFITS:
    - Simple and fast
    - No API costs
    - Easy to understand
    - Good for learning
    """

    def __init__(self):
        """Initialize with web research tools."""
        # Set up tools
        agent_tools = {
            'search': tools.search_web,
            'fetch': tools.fetch_webpage,
            'extract_text': tools.extract_text,
            'extract_links': tools.extract_links
        }

        super().__init__(agent_tools)
        print("[RESEARCH AGENT] Ready for research!")

    def research(self, question: str, num_sources: int = 1) -> Dict:
        """
        Research a question using web search.

        SIMPLE STRATEGY:
        1. Search Google
        2. Visit top results
        3. Extract text
        4. Return findings

        Args:
            question: The research question
            num_sources: How many websites to check (default: 1)

        Returns:
            Dictionary with:
            - question: The original question
            - sources: List of sources checked
            - findings: Extracted text from each source
            - summary: Combined findings
        """
        print(f"\n{'='*60}")
        print(f"RESEARCH QUESTION: {question}")
        print(f"{'='*60}\n")

        # STEP 1: Search Google
        print("[STEP 1] Searching Google...")
        search_results = self.execute_tool('search', query=question, num_results=num_sources)

        if not search_results or search_results[0].get('url') == '':
            return {
                'question': question,
                'sources': [],
                'findings': [],
                'summary': 'No results found'
            }

        # STEP 2: Visit each result and extract information
        sources = []
        findings = []

        for i, result in enumerate(search_results[:num_sources], 1):
            url = result['url']
            title = result['title']

            print(f"\n[STEP 2.{i}] Fetching: {title}")
            print(f"         URL: {url}")

            # Fetch the webpage
            page = self.execute_tool('fetch', url=url)

            if not page.get('success'):
                print(f"[WARNING] Could not fetch {url}")
                continue

            # Extract clean text
            print(f"[STEP 2.{i}] Extracting text...")
            text = self.execute_tool('extract_text', html=page['content'])

            # Limit text length for display
            preview = text[:500] + '...' if len(text) > 500 else text

            sources.append({
                'title': title,
                'url': url,
                'snippet': result.get('snippet', '')
            })

            findings.append({
                'source': title,
                'url': url,
                'text': text,
                'preview': preview
            })

            print(f"[SUCCESS] Extracted {len(text)} characters")

        # STEP 3: Create simple summary
        print(f"\n[STEP 3] Creating summary...")
        summary = self._create_simple_summary(question, findings)

        print(f"\n{'='*60}")
        print("RESEARCH COMPLETE")
        print(f"{'='*60}\n")

        return {
            'question': question,
            'sources': sources,
            'findings': findings,
            'summary': summary
        }

    def _create_simple_summary(self, question: str, findings: List[Dict]) -> str:
        """
        Create a simple summary without AI.

        SIMPLE APPROACH:
        - Shows source titles
        - Shows snippets
        - Provides text excerpts

        Note: Without AI, we can't truly "understand" or synthesize.
        We just organize the information nicely.
        """
        if not findings:
            return "No information found."

        summary_parts = [
            f"Research Results for: '{question}'",
            f"\nFound {len(findings)} source(s):\n"
        ]

        for i, finding in enumerate(findings, 1):
            summary_parts.append(f"\n{i}. {finding['source']}")
            summary_parts.append(f"   URL: {finding['url']}")
            summary_parts.append(f"   Preview: {finding['preview']}\n")

        summary_parts.append(f"\nNote: This is raw information from {len(findings)} source(s).")
        summary_parts.append("For true understanding and synthesis, consider using AI (Claude).")

        return '\n'.join(summary_parts)

    def quick_search(self, query: str) -> str:
        """
        Quick search - just returns Google snippets.
        Fastest option, no webpage fetching.

        Args:
            query: Search query

        Returns:
            Formatted search results
        """
        print(f"[QUICK SEARCH] {query}")

        results = self.execute_tool('search', query=query, num_results=3)

        output = [f"Quick search results for: '{query}'\n"]

        for i, result in enumerate(results, 1):
            output.append(f"{i}. {result['title']}")
            output.append(f"   {result['url']}")
            output.append(f"   {result['snippet']}\n")

        return '\n'.join(output)
