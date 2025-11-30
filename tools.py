"""Web search tools using Perplexity API."""
import requests
from typing import List, Dict
from config import Config


def perplexity_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Execute a single search query and return structured results."""
    try:
        print(f"  Calling Perplexity API for: {query[:50]}...")
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {Config.PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "sonar-pro",
                "messages": [
                    {"role": "system", "content": "You are a web search assistant. Provide factual information with sources."},
                    {"role": "user", "content": query}
                ],
                "temperature": 0.2,
                "max_tokens": 1000,
                "return_citations": True,
                "search_recency_filter": "month"
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        citations = data.get("citations", [])
        
        print(f"  Perplexity returned {len(citations)} citations, content length: {len(content)}")
        
        # Structure results with URL, title, and snippet
        results = [
            {"url": citation, "title": f"Source {i+1}", "snippet": content[:500] if i == 0 else ""}
            for i, citation in enumerate(citations[:max_results])
        ]
        
        if not results:
            print(f"  No citations, creating result from content")
            results = [{"url": "perplexity_response", "title": "Search Result", "snippet": content[:500]}]
        
        print(f"  Returning {len(results)} results")
        return results
        
    except Exception as e:
        print(f"  Perplexity API error: {e}")
        import traceback
        traceback.print_exc()
        return [{"url": "error", "title": "Search Error", "snippet": str(e)}]


def format_search_results(results: List[Dict[str, str]]) -> str:
    """Convert results to readable text for LLM consumption."""
    if not results:
        return "No results found."
    
    formatted = []
    for i, result in enumerate(results, 1):
        formatted.append(f"\n[{i}] {result.get('title', 'N/A')}")
        formatted.append(f"URL: {result.get('url', 'N/A')}")
        formatted.append(f"{result.get('snippet', 'N/A')}")
    return "\n".join(formatted)


def batch_search(queries: List[str], max_results_per_query: int = 5) -> Dict[str, List[Dict]]:
    """Execute multiple queries and aggregate results."""
    all_results = {}
    for query in queries:
        all_results[query] = perplexity_search(query, max_results=max_results_per_query)
    return all_results
