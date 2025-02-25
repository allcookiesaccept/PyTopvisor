from services.api import TopvisorAPI
from services.factory import ServiceFactory


class Topvisor:
    def __init__(self, user_id, api_key):
        self.api_client = TopvisorAPI(user_id, api_key)
        self.service_factory = ServiceFactory(self.api_client)

    def get_operation_mapping(self):
        """
        Возвращает словарь маппинга операций.
        Ключ: имя операции.
        Значение: кортеж (сервис, метод).
        """
        return {
            "get_projects": ("projects", "get_projects"),
            "get_competitors": ("projects", "get_competitors"),
            "get_history": ("positions", "get_history"),
            "get_summary": ("positions", "get_summary"),
            "get_summary_chart": ("positions", "get_summary_chart"),
            "get_searchers_regions": ("positions", "get_searchers_regions"),
        }

    def run_task(self, task_name, **kwargs):
        """
        Универсальный метод для выполнения операций.

        :param operation_name: Название операции.
        :param kwargs: Аргументы для операции.
        :return: Результат выполнения операции.
        """

        operation_mapping = self.get_operation_mapping()

        if task_name not in operation_mapping:
            raise ValueError(f"Unknown operation: {task_name}")

        service_name, method_name = operation_mapping[task_name]
        service = self.service_factory.get_service(service_name)

        method = getattr(service, method_name, None)

        if not method:
            raise AttributeError(
                f"Метод {method_name} не найден в сервисе {service_name}"
            )

        return method(**kwargs)




from config.settings import Config
config = Config()
tv = Topvisor(config.data.get("USER_ID"), config.data.get("TOPVISOR_API"))

