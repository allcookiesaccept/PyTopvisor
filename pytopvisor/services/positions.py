from pytopvisor.services.base import BaseService
from pytopvisor.utils.payload import PayloadFactory
from pytopvisor.utils.validators import Validator
from typing import List, Optional
from inspect import signature


class PositionsService(BaseService):

    def __init__(self, api_client):
        super().__init__(api_client)
        self.endpoints = {
            "history": "/v2/json/get/positions_2/history",
            "summary": "/v2/json/get/positions_2/summary",
            "summary_chart": "/v2/json/get/positions_2/summary/chart",
            "checker_price": "/v2/json/get/positions_2/checker/price",
            "searchers_regions_export": "/v2/json/get/positions_2/searchers/regions/export",
        }

    def get_positions_history(
        self,
        project_id: int,
        regions_indexes: List[int],
        dates: Optional[List[str]] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        competitors_ids: Optional[List[int]] = None,
        type_range: Optional[int] = None,
        count_dates: Optional[int] = None,
        only_exists_first_date: Optional[bool] = None,
        show_headers: Optional[bool] = None,
        show_exists_dates: Optional[bool] = None,
        show_visitors: Optional[bool] = None,
        show_top_by_depth: Optional[int] = None,
        positions_fields: Optional[List[str]] = None,
        filter_by_dynamic: Optional[List[str]] = None,
        filter_by_positions: Optional[List[List[int]]] = None,
        **kwargs
    ):
        """
        Retrieves the history of position checks.
        :param project_id: Project ID (required).
        :param regions_indexes: List of region indexes (required).
        :param dates: List of arbitrary check dates (in YYYY-MM-DD format).
        :param date1: Start date of the period (in YYYY-MM-DD format).
        :param date2: End date of the period (in YYYY-MM-DD format).
        :param competitors_ids: List of competitor IDs.
        :param type_range: Date range (enum: 0-7, 100).
        :param count_dates: Maximum number of returned dates (no more than 31).
        :param only_exists_first_date: Display only keywords present in the first check.
        :param show_headers: Add result headers.
        :param show_exists_dates: Add check dates.
        :param show_visitors: Add visitor data.
        :param show_top_by_depth: Add data for the specified depth of the TOP.
        :param positions_fields: Select columns of data with check results.
        :param filter_by_dynamic: Filter by keyword dynamics.
        :param filter_by_positions: Filter by keyword positions.
        :return: Request result.
        """

        Validator.validate("get_positions_history", **locals())
        payload = PayloadFactory.positions_get_history_payload(**locals())
        fetch_all = kwargs.get("fetch_all", False)
        limit = kwargs.get("limit", 10000)
        return self.send_request(self.endpoints["history"], payload, fetch_all=fetch_all, limit=limit)


    def get_positions_summary(
        self,
        project_id: int,
        region_index: int,
        dates: List[str],
        competitor_id: Optional[int] = None,
        only_exists_first_date: Optional[bool] = None,
        show_dynamics: Optional[bool] = None,
        show_tops: Optional[bool] = None,
        show_avg: Optional[bool] = None,
        show_visibility: Optional[bool] = None,
        show_median: Optional[bool] = None,
        **kwargs
    ):
        """
        Retrieves summary data for the selected project over two dates.
        :param project_id: Project ID.
        :param region_index: Region index.
        :param dates: List of two dates for building the summary.
        :param competitor_id: Competitor ID (optional).
        :param only_exists_first_date: Consider keywords present in both dates (boolean).
        :param show_dynamics: Add position dynamics (boolean).
        :param show_tops: Add TOP data (boolean).
        :param show_avg: Add average position (boolean).
        :param show_visibility: Add visibility (boolean).
        :param show_median: Add median position (boolean).
        :return: Request result.
        """

        Validator.validate("get_positions_summary", **locals())
        payload = PayloadFactory.positions_get_summary_payload(**locals())
        fetch_all = kwargs.get("fetch_all", False)
        limit = kwargs.get("limit", 10000)

        return self.send_request(self.endpoints["summary"], payload, fetch_all=fetch_all, limit=limit)



    def get_positions_summary_chart(
        self,
        project_id: int,
        region_index: int,
        dates: Optional[List[str]] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        competitors_ids: Optional[List[int]] = None,
        type_range: Optional[int] = None,
        only_exists_first_date: Optional[bool] = None,
        show_tops: Optional[bool] = None,
        show_avg: Optional[bool] = None,
        show_visibility: Optional[bool] = None,
        **kwargs
    ):
        """
        Retrieves data for the summary chart for the selected project.
        :param project_id: Project ID.
        :param region_index: Region index.
        :param dates: List of arbitrary check dates.
        :param date1: Start date of the period.
        :param date2: End date of the period.
        :param competitors_ids: List of competitor IDs (or project ID).
        :param type_range: Date range (enum: 0, 1, 2, 3, 4, 5, 6, 7, 100).
        :param only_exists_first_date: Consider keywords present in all dates (boolean).
        :param show_tops: Add TOP data (boolean).
        :param show_avg: Add average position (boolean).
        :param show_visibility: Add visibility (boolean).
        :return: Request result.
        """
        Validator.validate("get_positions_summary_chart", **locals())
        payload = PayloadFactory.positions_get_summary_chart_payload(**locals())
        fetch_all = kwargs.get("fetch_all", False)
        limit = kwargs.get("limit", 10000)
        return self.send_request(self.endpoints["summary_chart"], payload, fetch_all=fetch_all, limit=limit)


    def get_searchers_regions(
        self,
        project_id: int,
        searcher_key: Optional[int] = None,
        name_key: Optional[str] = None,
        country_code: Optional[str] = None,
        lang: Optional[str] = None,
        device: Optional[int] = None,
        depth: Optional[int] = None,
        **kwargs
    ):
        """
        Exports a list of regions added to the project.
        :param project_id: Project ID.
        :param searcher_key: Search engine key.
        :param name_key: Name or region key.
        :param country_code: Two-letter country code.
        :param lang: Interface language.
        :param device: Device type (enum: 0, 1, 2).
        :param depth: Check depth.
        :return: Request result.
        """
        Validator.validate("get_searchers_regions", **locals())
        payload = PayloadFactory.positions_get_searchers_regions_payload(**locals())

        return self.send_text_request(
            self.endpoints["searchers_regions_export"], payload
        )
