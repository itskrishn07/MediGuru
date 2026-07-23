import requests
import logging
from typing import Any, Dict, Optional, Tuple
from utils.constants import API_BASE_URL
from utils.session import get_auth_header

logger = logging.getLogger(__name__)

class APIService:
    """
    Production HTTP client wrapper for communicating with FastAPI backend endpoints.
    Provides typed methods for GET, POST, DELETE, and multipart file upload operations.
    """

    @staticmethod
    def get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Tuple[bool, Any]:
        """
        Sends a GET request to the specified backend endpoint.
        """
        url = f"{API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = get_auth_header()
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                return True, response.json()
            logger.warning(f"GET {url} returned status code {response.status_code}: {response.text}")
            return False, response.json().get("detail", f"Request failed with status code {response.status_code}")
        except Exception as e:
            logger.error(f"Network exception on GET {url}: {str(e)}")
            return False, f"Server connection failed: {str(e)}"

    @staticmethod
    def post(endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Tuple[bool, Any]:
        """
        Sends a POST JSON request to the specified backend endpoint.
        """
        url = f"{API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = get_auth_header()
        headers["Content-Type"] = "application/json"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            if response.status_code in (200, 201):
                return True, response.json()
            logger.warning(f"POST {url} returned status code {response.status_code}: {response.text}")
            return False, response.json().get("detail", f"Request failed with status code {response.status_code}")
        except Exception as e:
            logger.error(f"Network exception on POST {url}: {str(e)}")
            return False, f"Server connection failed: {str(e)}"

    @staticmethod
    def upload_file(endpoint: str, file_name: str, file_bytes: bytes, content_type: str) -> Tuple[bool, Any]:
        """
        Uploads a file via multipart form-data to the specified backend endpoint.
        """
        url = f"{API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = get_auth_header()
        files = {"file": (file_name, file_bytes, content_type)}
        try:
            response = requests.post(url, headers=headers, files=files, timeout=(30, 300))
            if response.status_code in (200, 201):
                return True, response.json()
            logger.warning(f"Upload {url} returned status code {response.status_code}: {response.text}")
            return False, response.json().get("detail", f"Upload failed with status code {response.status_code}")
        except requests.exceptions.Timeout:
            logger.error(f"Upload to {url} timed out after 300 seconds.")
            return False, "Processing timed out. The server is still processing your document in the background. Please check 'Reports History' in a moment."
        except Exception as e:
            logger.error(f"Network exception on upload to {url}: {str(e)}")
            return False, f"Upload connection failed: {str(e)}"

    @staticmethod
    def delete(endpoint: str) -> Tuple[bool, Any]:
        """
        Sends a DELETE request to the specified backend endpoint.
        """
        url = f"{API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = get_auth_header()
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            if response.status_code in (200, 204):
                return True, response.json() if response.text else {"message": "Deleted successfully"}
            logger.warning(f"DELETE {url} returned status code {response.status_code}: {response.text}")
            return False, response.json().get("detail", f"Delete failed with status code {response.status_code}")
        except Exception as e:
            logger.error(f"Network exception on DELETE {url}: {str(e)}")
            return False, f"Server connection failed: {str(e)}"
