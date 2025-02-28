
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

ERROR_MAPPING = {
    429: RateLimitError,
    503: ServerError,
    53: AuthenticationError,
    54: InvalidRequestError,
    1000: InvalidRequestError,
    1001: InvalidRequestError,
    1002: InvalidRequestError,
    1003: InvalidRequestError,
    1004: InvalidRequestError,
    2000: InvalidRequestError,
    2001: InvalidRequestError,
    2002: InvalidRequestError,
    2003: InvalidRequestError,
    2004: InvalidRequestError,
    2005: InvalidRequestError,
}