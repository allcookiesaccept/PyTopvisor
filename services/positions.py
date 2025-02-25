from .base import BaseService
from utils.payload import PayloadFactory
from typing import List, Any, Optional, Dict, Callable


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

    def get_history(
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
    ):
        """
        Получает историю проверки позиций.
        :param project_id: ID проекта (обязательный).
        :param regions_indexes: Список индексов регионов (обязательный).
        :param dates: Список произвольных дат проверок (в формате YYYY-MM-DD).
        :param date1: Начальная дата периода (в формате YYYY-MM-DD).
        :param date2: Конечная дата периода (в формате YYYY-MM-DD).
        :param competitors_ids: Список ID конкурентов.
        :param type_range: Период дат (enum: 0-7, 100).
        :param count_dates: Максимальное число возвращаемых дат (не более 31).
        :param only_exists_first_date: Отображать только ключевые фразы, присутствующие в первой проверке.
        :param show_headers: Добавить заголовки результатов.
        :param show_exists_dates: Добавить даты проверок.
        :param show_visitors: Добавить данные о количестве визитов.
        :param show_top_by_depth: Добавить данные по ТОПу указанной глубины.
        :param positions_fields: Выбор столбцов данных с результатами проверки.
        :param filter_by_dynamic: Фильтр по динамике ключевых фраз.
        :param filter_by_positions: Фильтр по позициям ключевых фраз.
        :return: Результат запроса.
        """
        # Валидация обязательных параметров
        if not isinstance(project_id, int):
            raise ValueError("project_id должен быть целым числом.")
        if not isinstance(regions_indexes, list) or not all(isinstance(idx, int) for idx in regions_indexes):
            raise ValueError("regions_indexes должен быть списком целых чисел.")

        # Валидация дат
        if dates and (date1 or date2):
            raise ValueError("Нельзя одновременно передавать 'dates' и 'date1/date2'.")
        if (date1 and not date2) or (date2 and not date1):
            raise ValueError("Необходимо указать оба параметра: 'date1' и 'date2'.")
        if dates and not all(isinstance(date, str) and len(date) == 10 for date in dates):
            raise ValueError("Все элементы в 'dates' должны быть строками в формате YYYY-MM-DD.")
        if date1 and not isinstance(date1, str) or date2 and not isinstance(date2, str):
            raise ValueError("Параметры 'date1' и 'date2' должны быть строками в формате YYYY-MM-DD.")

        # Формирование payload
        try:
            payload = PayloadFactory.positions_get_history_payload(
                project_id=project_id,
                regions_indexes=regions_indexes,
                dates=dates,
                date1=date1,
                date2=date2,
                competitors_ids=competitors_ids,
                type_range=type_range,
                count_dates=count_dates,
                only_exists_first_date=only_exists_first_date,
                show_headers=show_headers,
                show_exists_dates=show_exists_dates,
                show_visitors=show_visitors,
                show_top_by_depth=show_top_by_depth,
                positions_fields=positions_fields,
                filter_by_dynamic=filter_by_dynamic,
                filter_by_positions=filter_by_positions,
            )
        except Exception as e:
            raise RuntimeError(f"Ошибка при формировании payload: {e}")


        return self.send_request(self.endpoints["history"], payload)