from typing import List, Any, Optional, Dict, Callable
from functools import wraps


def add_universal_params(func: Callable) -> Callable:
    """
    Декоратор для добавления универсальных параметров в payload.
    Поддерживаемые параметры: limit, offset, fields, filters, id, orders.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        # Вызов основного метода для получения базового payload
        payload = func(*args, **kwargs)

        # Универсальные параметры
        universal_params = {
            "limit": int,
            "offset": int,
            "fields": list,
            "filters": dict,
            "id": int,
            "orders": list,
        }

        # Добавление универсальных параметров, если они переданы
        for param, param_type in universal_params.items():
            if param in kwargs:
                value = kwargs[param]
                if not isinstance(value, param_type):
                    raise ValueError(
                        f"Параметр '{param}' должен быть типа {param_type.__name__}"
                    )
                payload[param] = value

        return payload

    return wrapper


class PayloadFactory:

    @staticmethod
    @add_universal_params
    def projects_get_projects_payload(
            show_site_stat: Optional[bool] = None,
            show_searchers_and_regions: Optional[int] = None,
            include_positions_summary: Optional[bool] = None,
            ) -> Dict[str, Any] | None:

        """
        Генерирует payload для метода get/projects_2/projects.
        :param show_site_stat: Добавить дополнительную информацию о проекте (boolean).
        :param show_searchers_and_regions: Добавить список поисковых систем и регионов (0, 1, 2).
        :param include_positions_summary: Добавить сводку по позициям (boolean).
        :return: Payload для запроса.
        """
        payload = {}

        if show_site_stat:
            payload["show_site_stat"] = show_site_stat
        if show_searchers_and_regions:
            payload["show_searchers_and_regions"] = show_searchers_and_regions
        if include_positions_summary:
            payload["include_positions_summary"] = include_positions_summary

        return payload

    @staticmethod
    @add_universal_params
    def projects_get_competitors_payload(
            project_id: int,
            only_enabled: Optional[bool] = None,
            include_project: Optional[bool] = None,
    ) -> Dict[str, Any]:

        """
        Генерирует payload для метода get/projects_2/competitors.
        :param show_site_stat: Добавить дополнительную информацию о проекте (boolean).
        :param show_searchers_and_regions: Добавить список поисковых систем и регионов (0, 1, 2).
        :param include_positions_summary: Добавить сводку по позициям (boolean).
        :return: Payload для запроса.
        """
        payload = {
            "project_id": project_id,
        }

        if only_enabled:
            payload["only_enabled"] = only_enabled
        if include_project:
            payload["include_project"] = include_project

        return payload


    @staticmethod
    @add_universal_params
    def positions_get_history_payload(
            project_id: int,
            regions_indexes: List[int],
            dates: Optional[List[str]] = None,
            date1: Optional[str] = None,
            date2: Optional[str] = None,
            **kwargs,
    ) -> Dict[str, Any]:
        """
        Генерирует payload для метода positions_2/history

        Обязательные параметры:
        - project_id: int: ID проекта
        - regions_indexes: array(int): Список индексов регионов

        Необходимо указать либо:
        - dates: array of date: Список произвольных дат
        Или:
        - date1 и date2: date: Период проверок

        Дополнительные параметры:
        - fields: array fields: Возвращаемые поля объекта "Ключевая фраза"
        - competitors_ids: array(int): ID конкурентов (или ID проекта), добавленных в настройках проекта
        - type_range: enum(0, 1, 2, 3, 4, 5, 6, 7, 100): Период дат
        - count_dates: int: Максмальное число возвращаемых дат (не более 31)
        - only_exists_first_date: boolean: Отображать только ключевые фразы, присутствующие в первой проверке указанного периода
        - show_headers: boolean: Добавить в результат заголовки результатов
        - show_exists_dates: boolean: Добавить в результат даты, в которых были проверки
        - show_visitors: boolean: Добавить в результат данные об общем количество визитов по каждой проверке
        - show_top_by_depth: int: Добавить в результат данные по ТОПу указанной глубины по каждой проверке
        - positions_fields: array('position', 'snippet', 'relevant_url', 'visitors'): Выбор столбцов данных с результатами проверки
        - filter_by_dynamic: set('>', '<', '='): Фильтр по ключевым фразам
        - filter_by_positions: array of array(int, int): Фильтр по ключевым фразам, позиции которых входят в указанные промежутки
        """
        # Базовая структура payload
        payload: Dict[str, Any] = {
            "project_id": project_id,
            "regions_indexes": regions_indexes,
        }

        # Обработка дат
        if dates:
            payload["dates"] = dates
        elif date1 and date2:
            payload.update({"date1": date1, "date2": date2})
        else:
            raise ValueError("Необходимо указать либо 'dates', либо 'date1' и 'date2'")

        # Добавление опциональных параметров
        optional_params = [
            "fields",
            "competitors_ids",
            "type_range",
            "count_dates",
            "only_exists_first_date",
            "show_headers",
            "show_exists_dates",
            "show_visitors",
            "show_top_by_depth",
            "positions_fields",
            "filter_by_dynamic",
            "filter_by_positions",
        ]

        for param in optional_params:
            value = locals().get(param)
            if value is not None:
                payload[param] = value

        return payload