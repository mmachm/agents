import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Dict

def collect_data(source: str, parameters: Dict[str, str]) -> dict:
    """Collects data from various sources including web pages, APIs, and structured data.
    
    Args:
        source (str): Data source type ('webpage', 'api', 'csv', 'json')
        parameters (Dict[str, str]): Parameters for data collection
            - For webpage: 'url' required
            - For api: 'url' and 'method' required
            - For csv/json: 'path' required
            
    Returns:
        dict: Collected data and metadata
    """
    print(f"\n--- Tool Call: collect_data (source: {source}) ---")

    try:
        if source == "webpage":
            if "url" not in parameters:
                return {
                    "status": "error",
                    "error_message": "URL parameter required for webpage source",
                }

            # Fetch webpage content
            response = requests.get(parameters["url"])
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract text content
            text_content = soup.get_text(separator=" ", strip=True)

            # Extract links
            links = [a.get("href") for a in soup.find_all("a", href=True)]

            # Extract metadata
            metadata = {
                "title": soup.title.string if soup.title else None,
                "description": (
                    soup.find("meta", {"name": "description"}).get("content")
                    if soup.find("meta", {"name": "description"})
                    else None
                ),
                "domain": urlparse(parameters["url"]).netloc,
            }

            return {
                "status": "success",
                "data": {"content": text_content, "links": links, "metadata": metadata},
            }

        elif source == "api":
            if "url" not in parameters or "method" not in parameters:
                return {
                    "status": "error",
                    "error_message": "URL and method parameters required for API source",
                }

            # Prepare request parameters
            method = parameters["method"].upper()
            headers = json.loads(parameters.get("headers", "{}"))
            data = json.loads(parameters.get("data", "{}"))

            # Make API request
            response = requests.request(
                method=method,
                url=parameters["url"],
                headers=headers,
                json=data if method in ["POST", "PUT", "PATCH"] else None,
                params=data if method == "GET" else None,
            )
            response.raise_for_status()

            return {
                "status": "success",
                "data": {
                    "response": (
                        response.json()
                        if response.headers.get("content-type", "").startswith(
                            "application/json"
                        )
                        else response.text
                    ),
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                },
            }

        elif source == "csv":
            if "path" not in parameters:
                return {
                    "status": "error",
                    "error_message": "Path parameter required for CSV source",
                }

            # Read CSV file
            df = pd.read_csv(parameters["path"])

            # Convert to dictionary format
            data = {
                "columns": df.columns.tolist(),
                "rows": df.to_dict("records"),
                "shape": df.shape,
                "summary": {
                    "numeric_columns": df.describe().to_dict(),
                    "categorical_columns": {
                        col: df[col].value_counts().to_dict()
                        for col in df.select_dtypes(include=["object"]).columns
                    },
                },
            }

            return {"status": "success", "data": data}

        elif source == "json":
            if "path" not in parameters:
                return {
                    "status": "error",
                    "error_message": "Path parameter required for JSON source",
                }

            # Read JSON file
            with open(parameters["path"], "r") as f:
                data = json.load(f)

            return {"status": "success", "data": data}

        else:
            return {
                "status": "error",
                "error_message": f"Unsupported source type: {source}",
            }

    except Exception as e:
        return {"status": "error", "error_message": f"Error collecting data: {str(e)}"} 