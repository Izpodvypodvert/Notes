from enum import Enum


class NoteLimits(Enum):
    MAX_NOTES_PER_USER = 10
    TOO_MANY_NOTES_ERROR_MSG = (f"You cannot create more than "
                                f"{MAX_NOTES_PER_USER} notes.")


class CategoryLimits(Enum):
    MAX_Category_PER_USER = 3
    TOO_MANY_CATEGORIES_ERROR_MSG = (f"You cannot create more than "
                                     f"{MAX_Category_PER_USER} categories.")
