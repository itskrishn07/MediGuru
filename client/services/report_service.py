import logging
from typing import Tuple, Any, List, Optional
from services.api import APIService

logger = logging.getLogger(__name__)

class ReportService:
    """
    Handles report retrieval, details, and deletion from FastAPI backend:
    - GET /reports/
    - GET /reports/{report_id}
    - DELETE /reports/{report_id}
    """

    @staticmethod
    def get_all_reports() -> Tuple[bool, Any]:
        """
        Retrieves all uploaded medical reports for the authenticated user.
        """
        return APIService.get("reports/")

    @staticmethod
    def get_report_by_id(report_id: int) -> Tuple[bool, Any]:
        """
        Retrieves a single medical report with full extracted details & medicines.
        """
        return APIService.get(f"reports/{report_id}")

    @staticmethod
    def delete_report(report_id: int) -> Tuple[bool, Any]:
        """
        Deletes a medical report from PostgreSQL and ChromaDB.
        """
        return APIService.delete(f"reports/{report_id}")
