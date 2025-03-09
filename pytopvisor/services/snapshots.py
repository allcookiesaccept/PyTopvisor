from pytopvisor.services.base import BaseService
from pytopvisor.utils.payload import PayloadFactory
from pytopvisor.utils.validators import Validator
from typing import List, Optional
from inspect import signature


class SnapshotsService(BaseService):

    def __init__(self, api_service):
        super().__init__(api_service)
        self.endpoints = {
            "history": "/v2/json/get/snapshots_2/history",
            "competitors": "/v2/json/get/snapshots_2/competitors",
        }

    def get_snapshots_history(
        self,
        project_id: int,
        region_index: int,
        dates: Optional[List[str]] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        type_range: Optional[int] = None,
        count_dates: Optional[int] = None,
        show_exists_dates: Optional[bool] = None,
        show_ams: Optional[bool] = None,
        positions_fields: Optional[List[str]] = ["url", "domain", "snippet_title", "snippet_body"],
        **kwargs
    ):
        """
        Retrieves the history of position checks.
        :param project_id: Project ID (required).
        :param region_index: region index (required).
        :param dates: List of arbitrary check dates (in YYYY-MM-DD format).
        :param date1: Start date of the period (in YYYY-MM-DD format).
        :param date2: End date of the period (in YYYY-MM-DD format).
        :param type_range: Date range (enum: 0-7, 100).
        :param count_dates: Maximum number of returned dates (no more than 31).
        :param show_exists_dates: Add check dates.
        :param show_ams: Add to the result the storm index between the selected checks.
        :param positions_fields: Select columns of data with check results.
        :return: Request result.
        """
        Validator.validate("get_snapshots_history", **locals())
        payload = PayloadFactory.snapshots_get_history_payload(**locals())
        fetch_all = kwargs.get("fetch_all", False)
        limit = kwargs.get("limit", 10000)
        return self.send_request(self.endpoints["history"], payload, fetch_all=fetch_all, limit=limit)