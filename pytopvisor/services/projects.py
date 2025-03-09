from pytopvisor.services.base import BaseService
from pytopvisor.utils.payload import PayloadFactory
from pytopvisor.utils.validators import Validator
from typing import Optional


class ProjectsService(BaseService):
    def __init__(self, api_client):
        super().__init__(api_client)
        self.endpoints = {
            "projects": "/v2/json/get/projects_2/projects",
            "competitors": "/v2/json/get/projects_2/competitors",
        }

    def get_projects(
        self,
        show_site_stat: Optional[bool] = None,
        show_searchers_and_regions: Optional[int] = None,
        include_positions_summary: Optional[bool] = None,
        **kwargs
    ):
        """
        Retrieves a list of projects.
        """
        Validator.validate("get_projects", **locals())
        payload = PayloadFactory.projects_get_projects_payload(**locals())
        fetch_all = kwargs.get("fetch_all", False)
        limit = kwargs.get("limit", 10000)
        return self.send_request(self.endpoints["projects"], payload, fetch_all=fetch_all, limit=limit)

    def get_competitors(
        self,
        project_id: int,
        only_enabled: Optional[bool] = None,
        include_project: Optional[bool] = None,
        **kwargs
    ):
        """
        Retrieves a list of competitors.
        """
        Validator.validate("get_competitors", **locals())
        payload = PayloadFactory.projects_get_competitors_payload(**locals())
        fetch_all = kwargs.get("fetch_all", False)
        limit = kwargs.get("limit", 10000)
        return self.send_request(self.endpoints["competitors"], payload, fetch_all=fetch_all, limit=limit)
