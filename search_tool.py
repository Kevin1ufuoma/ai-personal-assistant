from duckduckgo_search import DDGS

def search_the_web(query: str, max_results: int = 3) -> str:
    """
    Searches DuckDuckGo for the query and returns a combined text string 
    of the top search result snippets. Completely free with no API keys.
    """
    print(f"Searching the web for: '{query}'...")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            
        if not results:
            return "No web search results found."
        
        combined_context = ""
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No Title')
            snippet = result.get('body', 'No Snippet')
            combined_context += f"Result {i}: [{title}] {snippet}\n"
            
        return combined_context
        
    except Exception as e:
        return f"Error executing live web search: {str(e)}"
