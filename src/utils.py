import json
from typing import Any


def read_json(json_file: str) -> Any:
    """Method to read JSON data"""

    with open(json_file, "r", encoding="UTF-8") as file:
        return json.load(file)