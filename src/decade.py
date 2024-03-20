from enum import Enum


class Decade(str, Enum):
    """
    A class to represent possible decades for music, starting from the 1950s.
    """
    FIFTIES = "1950s"
    SIXTIES = "1960s"
    SEVENTIES = "1970s"
    EIGHTIES = "1980s"
    NINETIES = "1990s"
    TWO_THOUSANDS = "2000s"
    TWENTY_TENS = "2010s"
    TWENTY_TWENTIES = "2020s"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, values : dict):
        if isinstance(value, cls):
            return value
        try:
            value = value.lower()
            if not value.endswith('s'):
                value += 's'
            return cls(value)
        except AttributeError:
            raise ValueError(f"Invalid value for Decade: {value}")