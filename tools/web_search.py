import json
import requests
from datetime import datetime
from typing import Dict

def search_web(query: str, max_results: int) -> dict:
    """Searches the web for information about a topic using DuckDuckGo.
    
    Args:
        query (str): The search query
        max_results (int): Maximum number of results to return
        
    Returns:
        dict: Search results and metadata
    """
    print(
        f"\n--- Tool Call: search_web (query: {query}, max_results: {max_results}) ---"
    )

    # DuckDuckGo API endpoint
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}

    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Parse the response
        data = response.json()

        # Extract relevant information
        results = []

        # Add the abstract if available
        if data.get("Abstract"):
            results.append(
                {
                    "title": data.get("Heading", ""),
                    "url": data.get("AbstractURL", ""),
                    "snippet": data.get("Abstract", ""),
                    "source": "DuckDuckGo",
                    "date": datetime.now().isoformat(),
                }
            )

        # Add related topics
        for topic in data.get("RelatedTopics", [])[:max_results]:
            if "Text" in topic and "FirstURL" in topic:
                results.append(
                    {
                        "title": topic.get("Text", "").split(" - ")[0],
                        "url": topic.get("FirstURL", ""),
                        "snippet": topic.get("Text", ""),
                        "source": "DuckDuckGo",
                        "date": datetime.now().isoformat(),
                    }
                )

        return {
            "status": "success",
            "data": {
                "results": results[:max_results],
                "metadata": {
                    "total_results": len(results),
                    "search_time": f"{response.elapsed.total_seconds():.2f}s",
                    "query": query,
                },
            },
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Error making API request: {str(e)}",
        }
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "error_message": f"Error parsing API response: {str(e)}",
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Unexpected error: {str(e)}"} 