import requests

def fetch_json(url, headers=None):
    """Fetch JSON data from an API endpoint."""
    try:
        if headers:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
