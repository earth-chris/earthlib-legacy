"""Errors and warnings"""


class SensorError(KeyError):
    """Raised when a function is not supported for a particular sensor"""

    pass


class EndmemberError(KeyError):
    """Raised when a function calls for an invalid land cover type"""

    pass
