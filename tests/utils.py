def strict_object(properties: dict) -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": [key for (key, value) in properties.items() if not value.get("optional")],
    }
