import requests
import json
import re
from typing import Optional, List, Dict
from .config import BASE_URL, HEADERS
from .utils import handle_response, parse_markdown

class Client:
    def __init__(self, api_access_token: str):
        self.headers = HEADERS.copy()
        self.headers["Authorization"] = f"ApiAccessToken {api_access_token}"

    def create_mem(self, content: str, is_read: Optional[bool] = False, is_archived: Optional[bool] = False,
                   scheduled_for: Optional[str] = None, created_at: Optional[str] = None,
                   mem_id: Optional[str] = None) -> dict:
        """
        Create a new mem with the specified parameters.

        :param content: The content of the mem.
        :param is_read: Whether the mem should be marked as read.
        :param is_archived: Whether the mem should be marked as archived.
        :param scheduled_for: The time the mem should resurface.
        :param created_at: The time the mem was created.
        :param mem_id: The ID to assign to the new mem.
        :return: The response from the API.
        """
        content = parse_markdown(content)
        payload = {
            "content": content,
            "isRead": is_read,
            "isArchived": is_archived,
            "scheduledFor": scheduled_for,
            "createdAt": created_at,
            "memId": mem_id
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(BASE_URL, headers=self.headers, data=json.dumps(payload))
        return handle_response(response)

    def create_mem_from_file(self, file_path: str) -> dict:
        """
        Create a new mem by uploading a markdown file.

        :param file_path: The path to the markdown file.
        :return: The response from the API.
        """
        headers = self.headers.copy()
        headers["Content-Type"] = "text/plain"
        with open(file_path, 'r') as file:
            content = file.read()
            content = parse_markdown(content)
            response = requests.post(BASE_URL, headers=headers, data=content)
            return handle_response(response)

    def batch_create_mems(self, mems: List[Dict[str, str]]) -> dict:
        """
        Batch create mems.

        :param mems: A list of dictionaries, each containing the content of a mem.
        :return: The response from the API.
        """
        for mem in mems:
            mem['content'] = parse_markdown(mem['content'])
        url = f"{BASE_URL}/batch"
        payload = json.dumps(mems)
        response = requests.post(url, headers=self.headers, data=payload)
        return handle_response(response)

    def append_to_mem(self, mem_id: str, content: str) -> dict:
        """
        Append content to an existing mem.

        :param mem_id: The ID of the mem to append to.
        :param content: The content to append.
        :return: The response from the API.
        """
        content = parse_markdown(content)
        url = f"{BASE_URL}/{mem_id}/append"
        payload = json.dumps({"content": content})
        response = requests.post(url, headers=self.headers, data=payload)
        return handle_response(response)
