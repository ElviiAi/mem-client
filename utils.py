import re
import requests

def handle_response(response: requests.Response) -> dict:
    if response.status_code == 400:
        raise ValueError("Bad Request: The request was invalid.")
    elif response.status_code == 401:
        raise PermissionError("Unauthorized: The API key token is not valid.")
    elif response.status_code == 404:
        raise FileNotFoundError("Not Found: The target resource was not found.")
    elif response.status_code == 429:
        raise ConnectionError("Rate Limited: This request exceeds the number of requests allowed. Slow down and try again.")
    elif response.status_code == 500:
        raise RuntimeError("Server Error: An unexpected error occurred. Please reach out to Mem support.")
    response.raise_for_status()
    return response.json()

def parse_markdown(content: str) -> str:
    unsupported_syntax = [
        r'\|',  # Tables
        r'<br>', r'<hr>',  # HTML tags
        r'>\s*>',  # Nested block quotes
    ]
    for syntax in unsupported_syntax:
        if re.search(syntax, content):
            raise ValueError(f"Unsupported markdown syntax found: {syntax}")
    content = re.sub(r'- \[ \]', r'* [ ]', content)  # Unchecked tasks
    content = re.sub(r'- \[x\]', r'* [x]', content)  # Checked tasks
    return content
