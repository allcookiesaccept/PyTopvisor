from typing import Dict, Any, List

class ValidationRules:
    RULES: Dict[str, Dict[str, Any]] = {
        "get_projects": {
            "show_site_stat": bool,
            "show_searchers_and_regions": int,
            "include_positions_summary": bool,
        },
        "get_competitors": {
            "project_id": int,
            "only_enabled": bool,
            "include_project": bool,
        },
        "get_positions_history": {
            "project_id": int,
            "regions_indexes": List[int],
            "dates": List[str],
            "date1": str,
            "date2": str,
            "competitors_ids": List[int],
            "type_range": int,
            "count_dates": int,
            "only_exists_first_date": bool,
            "show_headers": bool,
            "show_exists_dates": bool,
            "show_visitors": bool,
            "show_top_by_depth": int,
            "positions_fields": List[str],
            "filter_by_dynamic": List[str],
            "filter_by_positions": List[List[int]],
            "dates_date1_exclusive": ("validate_mutually_exclusive", "dates", "date1"),
            "date1_date2_pair": ("validate_required_pair", "date1", "date2"),
        },
        "get_positions_summary": {
            "project_id": int,
            "region_index": int,
            "dates": List[str],
            "competitor_id": int,
            "only_exists_first_date": bool,
            "show_dynamics": bool,
            "show_tops": bool,
            "show_avg": bool,
            "show_visibility": bool,
            "show_median": bool,
        },
        "get_positions_summary_chart": {
            "project_id": int,
            "region_index": int,
            "dates": List[str],
            "date1": str,
            "date2": str,
            "competitors_ids": List[int],
            "type_range": int,
            "only_exists_first_date": bool,
            "show_tops": bool,
            "show_avg": bool,
            "show_visibility": bool,
            "dates_date1_exclusive": ("validate_mutually_exclusive", "dates", "date1"),
            "date1_date2_pair": ("validate_required_pair", "date1", "date2"),
        },
        "get_searchers_regions": {
            "project_id": int,
            "searcher_key": int,
            "name_key": str,
            "country_code": str,
            "lang": str,
            "device": int,
            "depth": int,
        },
        "get_snapshots_history": {
            "project_id": int,
            "region_index": int,
            "dates": List[str],
            "date1": str,
            "date2": str,
            "type_range": int,
            "count_dates": int,
            "show_exists_dates": bool,
            "show_ams": bool,
            "positions_fields": List[str],
            "dates_date1_exclusive": ("validate_mutually_exclusive", "dates", "date1"),
            "date1_date2_pair": ("validate_required_pair", "date1", "date2"),
        },
    }

    @classmethod
    def get_rules(cls, method_name: str) -> Dict[str, Any]:
        if method_name not in cls.RULES:
            raise ValueError(f"No validation rules defined for method '{method_name}'")
        return cls.RULES[method_name]