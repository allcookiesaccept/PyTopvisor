import requests
from utils.logger import logger
from exceptions import *


class TopvisorAPI:
    def __init__(self, user_id, api_key):
        self.base_url = "https://api.topvisor.com"
        self.headers = {
            "Content-type": "application/json",
            "User-Id": user_id,
            "Authorization": f"bearer {api_key}",
        }

    def send_request(self, endpoint, payload):

        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            # Логирование успешного запроса
            logger.debug(f"Запрос к API выполнен успешно: {url}")

            # Попытка распарсить ответ как JSON
            try:
                data = response.json()
            except ValueError as e:
                logger.error(f"Ошибка парсинга JSON: {e}. Ответ: {response.text}")
                raise RuntimeError("Ответ от API не является валидным JSON.")

            # Проверка наличия ошибок в ответе
            if "errors" in data and data["errors"]:
                self._handle_api_errors(url, data["errors"])

            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к API: {e}")
            raise

    def send_text_request(self, endpoint, payload):
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.debug(f"Запрос к API выполнен успешно: {url}")
            return self.parse_text_response(response.text)

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к API: {e}")
            raise

    def parse_text_response(self, text, delimiter=";"):
        """
        Парсит текстовый ответ в формате CSV с указанным разделителем.
        :param text: Текстовый ответ от API.
        :param delimiter: Разделитель, используемый в тексте (по умолчанию ';').
        :return: Список списков с данными.
        """
        # Разделяем текст на строки
        decoded_text = text.encode('raw_unicode_escape').decode('cp1251')
        lines = decoded_text.strip().split("\n")
        result = []

        for line in lines:
            # Разделяем строку по указанному разделителю
            values = line.split(delimiter)
            result.append(values)

        return result

    def _handle_api_errors(self, url, errors):
        """
        Обрабатывает ошибки API и выбрасывает соответствующие исключения.
        """
        for error in errors:
            code = error.get("code")
            message = error.get("string", "Неизвестная ошибка")
            detail = error.get("detail", "")

            # Логирование ошибки
            logger.error(f"Ошибка API [{code}]: {message}. Подробности: {detail}. URL: {url}")

            # Выбор исключения на основе кода ошибки
            exception_class = ERROR_MAPPING.get(code, TopvisorAPIError)
            raise exception_class(f"[{code}] {message}. {detail}")