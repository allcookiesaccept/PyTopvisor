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
            competitors_ids: Optional[List[int]] = None,
            type_range: Optional[int] = 2,
            count_dates: Optional[int] = None,
            only_exists_first_date: Optional[bool] = None,
            show_headers: Optional[bool] = None,
            show_exists_dates: Optional[bool] = None,
            show_visitors: Optional[bool] = None,
            show_top_by_depth: Optional[int] = None,
            positions_fields: Optional[List[str]] = None,
            filter_by_dynamic: Optional[List[str]] = None,
            filter_by_positions: Optional[List[List[int]]] = None,
    ) -> Dict[str, Any]:
        """
        Генерирует payload для метода get/positions_2/history.

        :param project_id: ID проекта.
        :param regions_indexes: Список индексов регионов.
        :param dates: Список произвольных дат проверок.
        :param date1: Начальная дата периода.
        :param date2: Конечная дата периода.
        :param competitors_ids: Список ID конкурентов (или ID проекта).
        :param type_range: Период дат (enum: 0, 1, 2, 3, 4, 5, 6, 7, 100).
        :param count_dates: Максимальное число возвращаемых дат (не более 31).
        :param only_exists_first_date: Отображать только ключевые фразы, присутствующие в первой проверке.
        :param show_headers: Добавить заголовки результатов.
        :param show_exists_dates: Добавить даты, в которых были проверки.
        :param show_visitors: Добавить данные об общем количестве визитов.
        :param show_top_by_depth: Добавить данные по ТОПу указанной глубины.
        :param positions_fields: Выбор столбцов данных с результатами проверки.
        :param filter_by_dynamic: Фильтр по ключевым фразам.
        :param filter_by_positions: Фильтр по позициям ключевых фраз.
        :return: Payload для запроса.
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
            raise ValueError("Необходимо указать либо 'dates', либо 'date1' и 'date2'.")

        # Добавление опциональных параметров
        if competitors_ids:
            payload["competitors_ids"] = competitors_ids
        if type_range is not None:
            payload["type_range"] = type_range
        if count_dates is not None:
            payload["count_dates"] = count_dates
        if only_exists_first_date is not None:
            payload["only_exists_first_date"] = int(only_exists_first_date)
        if show_headers is not None:
            payload["show_headers"] = int(show_headers)
        if show_exists_dates is not None:
            payload["show_exists_dates"] = int(show_exists_dates)
        if show_visitors is not None:
            payload["show_visitors"] = int(show_visitors)
        if show_top_by_depth is not None:
            payload["show_top_by_depth"] = show_top_by_depth
        if positions_fields:
            payload["positions_fields"] = positions_fields
        if filter_by_dynamic:
            payload["filter_by_dynamic"] = filter_by_dynamic
        if filter_by_positions:
            payload["filter_by_positions"] = filter_by_positions

        return payload

    @staticmethod
    @add_universal_params
    def positions_get_summary_payload(
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
    ) -> Dict[str, Any]:
        """
        Генерирует payload для метода get/positions_2/summary.
        :param project_id: ID проекта.
        :param region_index: Индекс региона.
        :param dates: Список из двух дат для построения сводки.
        :param competitor_id: ID конкурента (опционально).
        :param only_exists_first_date: Учитывать ключевые фразы, присутствующие в обеих датах (boolean).
        :param show_dynamics: Добавить динамику позиций (boolean).
        :param show_tops: Добавить данные по ТОПам (boolean).
        :param show_avg: Добавить среднюю позицию (boolean).
        :param show_visibility: Добавить видимость (boolean).
        :param show_median: Добавить медианную позицию (boolean).
        :return: Payload для запроса.
        """
        # Базовая структура payload
        payload: Dict[str, Any] = {
            "project_id": project_id,
            "region_index": region_index,
            "dates": dates,
        }

        # Добавление опциональных параметров
        if competitor_id:
            payload["competitor_id"] = competitor_id
        if only_exists_first_date:
            payload["only_exists_first_date"] = int(only_exists_first_date)
        if show_dynamics:
            payload["show_dynamics"] = int(show_dynamics)
        if show_tops:
            payload["show_tops"] = int(show_tops)
        if show_avg:
            payload["show_avg"] = int(show_avg)
        if show_visibility:
            payload["show_visibility"] = int(show_visibility)
        if show_median:
            payload["show_median"] = int(show_median)

        return payload


    @staticmethod
    @add_universal_params
    def positions_get_summary_chart_payload(
        project_id: int,
        region_index: int,
        dates: Optional[List[str]] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        competitors_ids: Optional[List[int]] = None,
        type_range: Optional[int] = 2,
        only_exists_first_date: Optional[bool] = None,
        show_tops: Optional[bool] = None,
        show_avg: Optional[bool] = None,
        show_visibility: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Генерирует payload для метода get/positions_2/summary/chart.
        :param project_id: ID проекта.
        :param region_index: Индекс региона.
        :param dates: Список произвольных дат проверок.
        :param date1: Начальная дата периода.
        :param date2: Конечная дата периода.
        :param competitors_ids: Список ID конкурентов (или ID проекта).
        :param type_range: Период дат (enum: 0, 1, 2, 3, 4, 5, 6, 7, 100).
        :param only_exists_first_date: Учитывать ключевые фразы, присутствующие во всех датах (boolean).
        :param show_tops: Добавить данные по ТОПам (boolean).
        :param show_avg: Добавить среднюю позицию (boolean).
        :param show_visibility: Добавить видимость (boolean).
        :return: Payload для запроса.
        """
        # Базовая структура payload
        payload: Dict[str, Any] = {
            "project_id": project_id,
            "region_index": region_index,
        }

        # Обработка дат
        if dates:
            payload["dates"] = dates
        elif date1 and date2:
            payload.update({"date1": date1, "date2": date2})
        else:
            raise ValueError("Необходимо указать либо 'dates', либо 'date1' и 'date2'.")

        # Добавление опциональных параметров
        if competitors_ids:
            payload["competitors_ids"] = competitors_ids
        if type_range is not None:
            payload["type_range"] = type_range
        if only_exists_first_date is not None:
            payload["only_exists_first_date"] = int(only_exists_first_date)
        if show_tops is not None:
            payload["show_tops"] = int(show_tops)
        if show_avg is not None:
            payload["show_avg"] = int(show_avg)
        if show_visibility is not None:
            payload["show_visibility"] = int(show_visibility)

        return payload

    @staticmethod
    @add_universal_params
    def positions_get_searchers_regions_payload(
            project_id: int,
            searcher_key: Optional[int] = None,
            name_key: Optional[str] = None,
            country_code: Optional[str] = None,
            lang: Optional[str] = None,
            device: Optional[int] = None,
            depth: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Генерирует payload для метода get/positions_2/searchers/regions/export.
        :param project_id: ID проекта.
        :param searcher_key: Ключ поисковой системы.
        :param name_key: Название или ключ региона.
        :param country_code: Двухбуквенный код страны.
        :param lang: Язык интерфейса.
        :param device: Тип устройства (enum: 0, 1, 2).
        :param depth: Глубина проверки.
        :return: Payload для запроса.
        """
        # Базовая структура payload
        payload: Dict[str, Any] = {
            "project_id": project_id,
        }

        # Добавление опциональных параметров
        if searcher_key is not None:
            payload["searcher_key"] = searcher_key
        if name_key:
            payload["name/key"] = name_key
        if country_code:
            payload["country_code"] = country_code
        if lang:
            payload["lang"] = lang
        if device is not None:
            payload["device"] = device
        if depth is not None:
            payload["depth"] = depth

        return payload