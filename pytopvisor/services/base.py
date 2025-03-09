from abc import ABC


class BaseService(ABC):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client

    def send_request(self, endpoint, payload, fetch_all=False, limit=10000):
        """
        Sends a request to the API, optionally fetching all paginated data.
        :param endpoint: API endpoint.
        :param payload: Request payload.
        :param fetch_all: If True, fetch all paginated data.
        :param limit: Pagination limit (used if fetch_all=True).
        :return: API response or list of all results if fetch_all=True.
        """
        if fetch_all:
            return self.api_client.fetch_all(endpoint, payload, limit=limit)
        return self.api_client.send_request(endpoint, payload)

    def send_text_request(self, endpoint, payload):

        return self.api_client.send_text_request(endpoint, payload)

