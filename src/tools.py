"""
Web Research Tools
==================
These are the individual capabilities (tools) your agent can use.
Each function does ONE specific task.

"""

import os
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from urllib.parse import urljoin


def fetch_webpage(url: str, timeout: int = 10) -> Dict:
    
    try:
        response = requests.get(
            url, 
            timeout=timeout,
            headers={'User-Agent': 'ResearchBot/1.0 (Educational Project)'}
        )
        
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
    
    # Parse the HTML (turn it into a structure we can work with)
    soup = BeautifulSoup(html, 'lxml')
    
    # Remove elements that aren't useful content
    for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
        element.decompose()
    
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
    
    soup = BeautifulSoup(html, 'lxml')
    links = []
    
    # Find all <a> tags that have an href attribute
    for link in soup.find_all('a', href=True):
        href = link['href']
        text = link.get_text(strip=True)
        
        # Convert relative URLs to absolute
        if not href.startswith('http'):
            href = urljoin(base_url, href)
        
        # Only include actual web links (not mailto:, javascript:, etc.)
        if href.startswith('http'):
            links.append({
                'url': href,
                'text': text or '(no text)'
            })
    
    return links


def search_web(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    
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
