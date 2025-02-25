
class TopvisorAPIError(Exception):
    """Базовое исключение для API Topvisor."""
    pass

class AuthenticationError(TopvisorAPIError):
    """Исключение для ошибок аутентификации."""
    pass

class RateLimitError(TopvisorAPIError):
    """Исключение для ошибок превышения лимитов запросов."""
    pass

class InvalidRequestError(TopvisorAPIError):
    """Исключение для ошибок валидации запроса."""
    pass

class ServerError(TopvisorAPIError):
    """Исключение для серверных ошибок."""
    pass