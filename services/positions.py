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

    def get_summary(
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
    ):
        """
        Получает данные сводки по выбранному проекту за две даты.
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
        :return: Результат запроса.
        """
        # Валидация обязательных параметров
        if not isinstance(project_id, int):
            raise ValueError("project_id должен быть целым числом.")
        if not isinstance(region_index, int):
            raise ValueError("region_index должен быть целым числом.")
        if not isinstance(dates, list) or len(dates) != 2:
            raise ValueError("dates должен быть списком из двух дат.")
        if not all(isinstance(date, str) and len(date) == 10 for date in dates):
            raise ValueError("Все элементы в 'dates' должны быть строками в формате YYYY-MM-DD.")

        # Формирование payload
        try:
            payload = PayloadFactory.positions_get_summary_payload(
                project_id=project_id,
                region_index=region_index,
                dates=dates,
                competitor_id=competitor_id,
                only_exists_first_date=only_exists_first_date,
                show_dynamics=show_dynamics,
                show_tops=show_tops,
                show_avg=show_avg,
                show_visibility=show_visibility,
                show_median=show_median,
            )
        except Exception as e:
            raise RuntimeError(f"Ошибка при формировании payload: {e}")

        return self.send_request(self.endpoints["summary"], payload)

    def get_summary_chart(
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
    ):
        """
        Получает данные для графика сводки по выбранному проекту.
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
        :return: Результат запроса.
        """
        # Валидация обязательных параметров
        if not isinstance(project_id, int):
            raise ValueError("project_id должен быть целым числом.")
        if not isinstance(region_index, int):
            raise ValueError("region_index должен быть целым числом.")
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
            payload = PayloadFactory.positions_get_summary_chart_payload(
                project_id=project_id,
                region_index=region_index,
                dates=dates,
                date1=date1,
                date2=date2,
                competitors_ids=competitors_ids,
                type_range=type_range,
                only_exists_first_date=only_exists_first_date,
                show_tops=show_tops,
                show_avg=show_avg,
                show_visibility=show_visibility,
            )
        except Exception as e:
            raise RuntimeError(f"Ошибка при формировании payload: {e}")

        return self.send_request(self.endpoints["summary_chart"], payload)

    def get_searchers_regions(
            self,
            project_id: int,
            searcher_key: Optional[int] = None,
            name_key: Optional[str] = None,
            country_code: Optional[str] = None,
            lang: Optional[str] = None,
            device: Optional[int] = None,
            depth: Optional[int] = None,
    ):
        """
        Экспортирует список регионов, добавленных в проект.
        :param project_id: ID проекта.
        :param searcher_key: Ключ поисковой системы.
        :param name_key: Название или ключ региона.
        :param country_code: Двухбуквенный код страны.
        :param lang: Язык интерфейса.
        :param device: Тип устройства (enum: 0, 1, 2).
        :param depth: Глубина проверки.
        :return: Результат запроса.
        """
        # Валидация параметров
        if not isinstance(project_id, int):
            raise ValueError("project_id должен быть целым числом.")
        if searcher_key and not isinstance(searcher_key, int):
            raise ValueError("searcher_key должен быть целым числом.")
        if name_key and not isinstance(name_key, str):
            raise ValueError("name_key должен быть строкой.")
        if country_code and (not isinstance(country_code, str) or len(country_code) != 2):
            raise ValueError("country_code должен быть двухбуквенным кодом страны.")
        if lang and not isinstance(lang, str):
            raise ValueError("lang должен быть строкой.")
        if device is not None and device not in (0, 1, 2):
            raise ValueError("device должен быть одним из значений: 0, 1, 2.")
        if depth is not None and not isinstance(depth, int):
            raise ValueError("depth должен быть целым числом.")

        # Формирование payload
        try:
            payload = PayloadFactory.positions_get_searchers_regions_payload(
                project_id=project_id,
                searcher_key=searcher_key,
                name_key=name_key,
                country_code=country_code,
                lang=lang,
                device=device,
                depth=depth,
            )
        except Exception as e:
            raise RuntimeError(f"Ошибка при формировании payload: {e}")

        return self.send_text_request(self.endpoints["searchers_regions_export"], payload)