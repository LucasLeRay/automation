from enum import Enum


class StrEnum(str, Enum):
    """An enhanced version of Enum, to nicely work with strings.

    See https://www.cosmicpython.com/blog/2020-10-27-i-hate-enums.html
    """
    def __str__(self):
        return str.__str__(self)

    def __repr__(self):
        return f"{self.__class__.__name__}('{str(self)}')"

    def _generate_next_value_(name, start, count, last_values):
        return name
