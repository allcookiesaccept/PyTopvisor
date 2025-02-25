import requests
from utils.logger import logger


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

            if response.status_code != 200:
                raise RuntimeError(f"API вернул ошибку: {response.status_code}, {response.text}")
            try:
                logger.debug(f"Запрос к API выполнен успешно: {url}")
                return response.json()
            except ValueError:
                return self.parse_text_response(response.text)
            return response.json()
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