import os
import json
import urllib.parse
from typing import Dict, List, Optional, Tuple, Union

import requests
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class BrightDataSearchInput(BaseModel):
    """Input schema for Bright Data search."""
    query: str = Field(description="Search query string")


class BrightDataSearchWrapper:
    """Wrapper for Bright Data SERP API."""
    
    def __init__(self, api_key: Optional[str] = None, zone: Optional[str] = None):
        self.api_key = api_key or os.getenv("BRIGHT_DATA_API_KEY")
        self.zone = zone or os.getenv("BRIGHT_DATA_ZONE", "unblocker")
        self.default_engine = os.getenv("BRIGHT_DATA_DEFAULT_ENGINE", "google")
        
        if not self.api_key:
            raise ValueError("Bright Data API key not found. Set BRIGHT_DATA_API_KEY environment variable.")
    
    def _get_search_url(self, engine: str, query: str) -> str:
        """Generate the search URL based on the engine."""
        q = urllib.parse.quote(query)
        
        if engine == "yandex":
            return f"https://yandex.com/search/?text={q}"
        elif engine == "bing":
            return f"https://www.bing.com/search?q={q}"
        else:  # default to google
            return f"https://www.google.com/search?q={q}"
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def search(
        self,
        query: str,
        engine: Optional[str] = None,
        max_results: Optional[int] = 10
    ) -> Dict:
        """Perform search using Bright Data API.
        
        Args:
            query: Search query
            engine: Search engine to use (google, bing, yandex)
            max_results: Maximum number of results (not directly used, but kept for compatibility)
            
        Returns:
            Dictionary with search results in markdown format
        """
        engine = engine or self.default_engine
        url = self._get_search_url(engine, query)
        
        request_data = {
            "url": url,
            "zone": self.zone,
            "format": "raw",
            "data_format": "markdown"
        }
        
        try:
            response = requests.post(
                "https://api.brightdata.com/request",
                json=request_data,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            # Return markdown results directly
            return {
                "results": response.text,
                "engine": engine,
                "query": query
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Error performing search: {str(e)}",
                "results": "",
                "engine": engine,
                "query": query
            }
    
    async def search_async(
        self,
        query: str,
        engine: Optional[str] = None,
        max_results: Optional[int] = 10
    ) -> Dict:
        """Async version of search. Currently just wraps sync version."""

        return self.search(query, engine, max_results)


class BrightDataSearchResults(BaseTool):
    """Tool for searching using Bright Data SERP API."""
    
    name: str = "bright_data_search"
    description: str = (
        "Search the web using Bright Data's SERP API. "
        "Returns search results in markdown format from Google, Bing, or Yandex."
    )
    args_schema: Type[BaseModel] = BrightDataSearchInput  
    
    max_results: int = Field(default=10, description="Maximum number of results")
    search_engine: str = Field(default="google", description="Search engine to use")
    api_wrapper: BrightDataSearchWrapper = Field(default_factory=BrightDataSearchWrapper)
    
    def _format_results(self, raw_results: Dict) -> str:
        """Format the markdown results and extract URLs for frontend compatibility."""
        if raw_results.get("error"):
            return json.dumps({"error": raw_results['error'], "results": []})
        
        markdown_content = raw_results.get("results", "")
        if not markdown_content:
            return json.dumps({"results": []})
        
        # Extract URLs from markdown using regex
        import re
        url_pattern = r'https?://[^\s\)]+(?:\([^\)]*\))?[^\s\)\]]*'
        urls = re.findall(url_pattern, markdown_content)
        clean_urls = [url.rstrip(')') for url in urls]
        
        # ✅ CREATE ONLY ONE RESULT ENTRY, NOT ONE PER URL
        return json.dumps({
            "results": [{"url": clean_urls[0] if clean_urls else ""}],  # Just first URL
            "urls": clean_urls,  # All URLs for frontend
            "markdown": markdown_content
        })
    
    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Execute the search and return JSON string."""
        try:
            raw_results = self.api_wrapper.search(
                query=query,
                engine=self.search_engine,
                max_results=self.max_results
            )
            
            formatted_results = self._format_results(raw_results)
            
            if not formatted_results or formatted_results.strip() == "":
                return json.dumps({"error": "Empty search results", "results": []})
                
            return formatted_results
            
        except Exception as e:
            return json.dumps({"error": str(e), "results": []})

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:  # Changed return type to str
        """Execute the search asynchronously."""
        try:
            raw_results = await self.api_wrapper.search_async(
                query=query,
                engine=self.search_engine,
                max_results=self.max_results
            )
            
            formatted_results = self._format_results(raw_results)
            print(f"Bright Data async search for '{query}' using {self.search_engine}")
            return formatted_results  # Return string directly
            
        except Exception as e:
            error_msg = f"Error in Bright Data async search: {str(e)}"
            return error_msg  # Return string directly


if __name__ == "__main__":
    # Test the implementation
    wrapper = BrightDataSearchWrapper()
    results = wrapper.search("cute panda", engine="google")
    print(json.dumps(results, indent=2, ensure_ascii=False))