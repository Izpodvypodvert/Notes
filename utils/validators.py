def validate_note_title(title: str) -> bool:
    if not title or len(title) < 3:
        raise ValueError(
            "The course title must be at least 3 characters long.")
    return True
