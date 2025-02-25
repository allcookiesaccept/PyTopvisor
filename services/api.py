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
            logger.debug(f"Запрос к API выполнен успешно: {url}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к API: {e}")
            raise



