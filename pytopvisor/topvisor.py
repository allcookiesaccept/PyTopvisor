from pytopvisor.services.api import TopvisorAPI
from pytopvisor.services.factory import ServiceFactory


class Topvisor:
    def __init__(self, user_id, api_key):
        self.api_client = TopvisorAPI(user_id, api_key)
        self.service_factory = ServiceFactory(self.api_client)

    def get_operation_mapping(self):
        """
        Returns a dictionary mapping operations.
        Key: operation name.
        Value: tuple (service, method).
        """
        return {
            "get_projects": ("projects", "get_projects"),
            "get_competitors": ("projects", "get_competitors"),
            "get_positions_history": ("positions", "get_positions_history"),
            "get_positions_summary": ("positions", "get_positions_summary"),
            "get_positions_summary_chart": ("positions", "get_positions_summary_chart"),
            "get_searchers_regions": ("positions", "get_searchers_regions"),
            "get_snapshots_history": ("snapshots", "get_snapshots_history"),
        }

    def run_task(self, task_name, fetch_all=False, limit=10000, **kwargs):
        """
        Universal method for executing operations.
        :param task_name: Operation name.
        :param fetch_all: If True, fetch all paginated data (default: False).
        :param limit: Number of items per request if fetch_all=True (default: 10000).
        :param kwargs: Arguments for the operation.
        :return: Operation execution result (single response or all paginated data).
        """

        operation_mapping = self.get_operation_mapping()

        if task_name not in operation_mapping:
            raise ValueError(f"Unknown operation: {task_name}")

        service_name, method_name = operation_mapping[task_name]
        service = self.service_factory.get_service(service_name)

        method = getattr(service, method_name, None)

        if not method:
            raise AttributeError(
                f"Method {method_name} not found in service {service_name}"
            )
        kwargs["fetch_all"] = fetch_all
        kwargs["limit"] = limit
        return method(**kwargs)