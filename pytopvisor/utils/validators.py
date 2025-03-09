from typing import Any, List, get_origin, get_args
from datetime import datetime
from pytopvisor.utils.validation_rules import ValidationRules

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class Validator:
    """Flexible parameter validator for Topvisor API methods."""

    @staticmethod
    def validate_type(value: Any, expected_type: Any, param_name: str) -> None:
        if value is None:
            return
        # Проверяем, является ли expected_type generic-типом (например, List[str])
        origin_type = get_origin(expected_type) or expected_type
        if origin_type is list:
            if not isinstance(value, list):
                raise ValidationError(f"'{param_name}' must be a list")
            # Получаем тип элементов списка (например, str из List[str])
            item_type = get_args(expected_type)[0]
            if item_type is not Any:  # Пропускаем Any, если нет строгого типа
                for item in value:
                    Validator.validate_type(item, item_type, f"element of {param_name}")
        elif not isinstance(value, origin_type):
            raise ValidationError(f"'{param_name}' must be {origin_type.__name__}")

    @staticmethod
    def validate_string_length(value: str, length: int, param_name: str) -> None:
        if value is None:
            return
        if not isinstance(value, str):
            raise ValidationError(f"'{param_name}' must be a string")
        if len(value) != length:
            raise ValidationError(f"'{param_name}' must be {length} characters long")

    @staticmethod
    def validate_date(date_str: str, param_name: str) -> None:
        if date_str is None:
            return
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            if len(date_str) != 10:
                raise ValueError
        except ValueError:
            raise ValidationError(f"'{param_name}' must be in YYYY-MM-DD format")

    @staticmethod
    def validate_date_list(dates: List[str], param_name: str) -> None:
        if dates is None:
            return
        Validator.validate_type(dates, List[str], param_name)
        for date in dates:
            Validator.validate_date(date, f"element of {param_name}")

    @staticmethod
    def validate_enum(value: Any, allowed_values: List[Any], param_name: str) -> None:
        if value is not None and value not in allowed_values:
            raise ValidationError(f"'{param_name}' must be one of {allowed_values}")

    @staticmethod
    def validate_mutually_exclusive(param1: Any, param1_name: str, param2: Any, param2_name: str) -> None:
        if param1 is not None and param2 is not None:
            raise ValidationError(f"Cannot provide both '{param1_name}' and '{param2_name}'")

    @staticmethod
    def validate_required_pair(param1: Any, param1_name: str, param2: Any, param2_name: str) -> None:
        if (param1 is not None and param2 is None) or (param2 is not None and param1 is None):
            raise ValidationError(f"Both '{param1_name}' and '{param2_name}' must be provided together")

    @classmethod
    def validate(cls, method_name: str, **kwargs) -> None:
        """Validates parameters based on predefined rules for the method."""
        rules = ValidationRules.get_rules(method_name)

        # Проверка основных параметров
        for param_name, rule in rules.items():
            if param_name.endswith("_exclusive") or param_name.endswith("_pair"):
                continue
            value = kwargs.get(param_name)
            if isinstance(rule, tuple):
                expected_type = rule[0]
                cls.validate_type(value, expected_type, param_name)
                if len(rule) > 1 and value is not None:
                    if rule[1] == "validate_list_type":
                        cls.validate_type(value, expected_type, param_name)  # Уже обработано в validate_type
                    elif rule[1] == "validate_date":
                        cls.validate_date(value, param_name)
                    elif rule[1] == "validate_date_list":
                        cls.validate_date_list(value, param_name)
                    elif rule[1] == "validate_string_length":
                        cls.validate_string_length(value, 2, param_name)
                    elif rule[1].startswith("validate_enum"):
                        allowed_values = rule[2]
                        cls.validate_enum(value, allowed_values, param_name)
                    else:
                        raise ValueError(f"Unknown validator {rule[1]} for {param_name}")
            else:
                cls.validate_type(value, rule, param_name)

        # Проверка взаимоисключений и пар
        for param_name, rule in rules.items():
            if param_name.endswith("_exclusive"):
                validator_name, param1, param2 = rule
                if validator_name == "validate_mutually_exclusive":
                    cls.validate_mutually_exclusive(kwargs.get(param1), param1, kwargs.get(param2), param2)
            elif param_name.endswith("_pair"):
                validator_name, param1, param2 = rule
                if validator_name == "validate_required_pair":
                    cls.validate_required_pair(kwargs.get(param1), param1, kwargs.get(param2), param2)