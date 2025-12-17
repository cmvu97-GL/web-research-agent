"""
Web Research Tools
==================
These are the individual capabilities (tools) your agent can use.
Each function does ONE specific task.

Think of these as the agent's "hands" - ways to interact with the web.
"""

import os
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from urllib.parse import urljoin


def fetch_webpage(url: str, timeout: int = 10) -> Dict:
    """
    Downloads a webpage from the internet.

     WHY THIS EXISTS:
    - Agents need to get information from websites
    - This handles all the technical details of HTTP requests
    - Returns structured data (dictionary) that's easy to work with

    HOW IT WORKS:
    1. Makes an HTTP GET request (like typing URL in browser)
    2. Waits up to 'timeout' seconds for response
    3. If successful, returns the HTML content
    4. If it fails, returns an error message

    Args:
        url: The website address to fetch (e.g., "https://example.com")
        timeout: How many seconds to wait before giving up (default: 10)
    
    Returns:
        Dictionary with these keys:
        - success: True if it worked, False if it failed
        - content: The HTML content (if successful)
        - status_code: HTTP status (200 = OK, 404 = Not Found, etc.)
        - error: Error message (if it failed)

    Example:
        result = fetch_webpage("https://example.com")
        if result['success']:
            print(result['content'])  # The HTML
        else:
            print(result['error'])    # What went wrong
    """
    try:
        # Make the HTTP request
        # headers = tells the website we're a bot (polite!)
        response = requests.get(
            url, 
            timeout=timeout,
            headers={'User-Agent': 'ResearchBot/1.0 (Educational Project)'}
        )
        
        # raise_for_status() checks if request was successful
        # Raises an error for status codes like 404, 500, etc.
        response.raise_for_status()

        # Success! Return the data
        return {
            'success': True,
            'content': response.text,      # The HTML content
            'status_code': response.status_code,  # Usually 200
            'error': None
        }
        
    except requests.Timeout:
        # The website took too long to respond
        return {
            'success': False,
            'content': None,
            'status_code': None,
            'error': f'Timeout: Website did not respond within {timeout} seconds'
        }
        
    except requests.RequestException as e:
        # Something else went wrong (no internet, bad URL, etc.)
        return {
            'success': False,
            'content': None,
            'status_code': None,
            'error': f'Request failed: {str(e)}'
        }


def extract_text(html: str) -> str:
    """
    Converts messy HTML into clean, readable text.
    
    WHY THIS EXISTS:
    - HTML has lots of tags: <div>, <script>, <style>, etc.
    - We only want the actual readable content
    - AI models work better with clean text than raw HTML
    
    HOW IT WORKS:
    1. Parse HTML using BeautifulSoup (HTML parser)
    2. Remove unwanted elements (scripts, styles, navigation)
    3. Extract just the text
    4. Clean up extra whitespace
    
    Args:
        html: Raw HTML string (from fetch_webpage)
    
    Returns:
        Clean text string without HTML tags
    
    Example:
        html = "<html><body><h1>Hello</h1><p>World</p></body></html>"
        text = extract_text(html)
        # Result: "Hello\nWorld"
    """
    # Parse the HTML (turn it into a structure we can work with)
    soup = BeautifulSoup(html, 'lxml')
    
    # Remove elements that aren't useful content
    # These usually contain navigation, ads, styling, code
    for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
        element.decompose()  # Remove from the document
    
    # Get all the text, separated by newlines
    text = soup.get_text(separator='\n')
    
    # Clean up whitespace:
    # 1. Split into lines
    # 2. Strip whitespace from each line
    # 3. Remove empty lines
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    clean_text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return clean_text


def extract_links(html: str, base_url: str) -> List[Dict[str, str]]:
    """
    Finds all links on a webpage.
    
    WHY THIS EXISTS:
    - Research often requires following links to related pages
    - Lets the agent discover more information sources
    - Useful for building a web of connected information
    
    HOW IT WORKS:
    1. Parse HTML to find all <a> tags (links)
    2. Extract the URL and link text
    3. Convert relative URLs to absolute URLs
    4. Return as a list of dictionaries
    
    Args:
        html: Raw HTML string
        base_url: The page's URL (needed to resolve relative links)
                  Example: if link is "/about" and base is "https://example.com"
                  Result will be "https://example.com/about"
    
    Returns:
        List of dictionaries, each with:
        - url: The full URL
        - text: The clickable text of the link
    
    Example:
        html = '<a href="/page">Click me</a>'
        links = extract_links(html, "https://example.com")
        # Result: [{'url': 'https://example.com/page', 'text': 'Click me'}]
    """
    soup = BeautifulSoup(html, 'lxml')
    links = []
    
    # Find all <a> tags that have an href attribute
    for link in soup.find_all('a', href=True):
        href = link['href']
        text = link.get_text(strip=True)
        
        # Convert relative URLs to absolute
        # Relative: "/about" or "../contact"
        # Absolute: "https://example.com/about"
        if not href.startswith('http'):
            href = urljoin(base_url, href)
        
        # Only include actual web links (not mailto:, javascript:, etc.)
        if href.startswith('http'):
            links.append({
                'url': href,
                'text': text or '(no text)'  # Some links have no text
            })
    
    return links


def search_web(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Searches the web using DuckDuckGo HTML scraping.

    WHY THIS EXISTS:
    - Agents need to find relevant websites for a topic
    - This is how research starts - finding sources
    - Uses DuckDuckGo (no API key required!)

    HOW IT WORKS:
    1. Makes a request to DuckDuckGo HTML search
    2. Parses the HTML to extract search results
    3. Returns structured data (title, URL, snippet)
    4. Handles errors gracefully

    Args:
        query: What to search for (e.g., "Python web scraping")
        num_results: How many results to return (default: 5, max: 10)

    Returns:
        List of search results, each with:
        - title: Page title
        - url: Page URL
        - snippet: Short description/preview

    Example:
        results = search_web("Python tutorials")
        for result in results:
            print(f"{result['title']}: {result['url']}")
    """
    try:
        print(f"[SEARCH] Searching DuckDuckGo for: '{query}'")

        # DuckDuckGo HTML search URL
        url = "https://html.duckduckgo.com/html/"

        # Search parameters
        params = {
            'q': query
        }

        # Make the request with headers to look like a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.post(url, data=params, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'lxml')

        # Find search result elements
        results = soup.find_all('div', class_='result')

        search_results = []

        for result in results[:num_results]:
            # Extract title
            title_elem = result.find('a', class_='result__a')
            title = title_elem.get_text(strip=True) if title_elem else 'No title'

            # Extract URL
            url_elem = result.find('a', class_='result__url')
            result_url = url_elem.get('href') if url_elem else ''

            # Extract snippet
            snippet_elem = result.find('a', class_='result__snippet')
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else 'No description'

            if result_url:  # Only add if we have a URL
                search_results.append({
                    'title': title,
                    'url': result_url,
                    'snippet': snippet
                })

        if not search_results:
            print(f"[SEARCH] No results found for: '{query}'")
            return [{
                'title': 'No results found',
                'url': '',
                'snippet': f'No search results for "{query}"'
            }]

        print(f"[SEARCH] Found {len(search_results)} results")
        return search_results

    except Exception as e:
        # Handle any errors (network issues, parsing errors, etc.)
        print(f"[ERROR] Search failed: {str(e)}")
        return [{
            'title': 'Search Error',
            'url': '',
            'snippet': f'Search failed: {str(e)}'
        }]
