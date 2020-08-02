BIRD_SCHEMA = {
    "type": "object",
    "properties": {
        "species": {"type": "string"},
        "name": {"type": "string"},
        "color": {"type": "string"},
        "body_length": {"type": "integer"},
        "wingspan": {"type": "integer"}
    },
    "required": ["species", "name", "color", "body_length", "wingspan"],
}
