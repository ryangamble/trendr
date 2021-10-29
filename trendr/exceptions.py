class TrendrException(Exception):
    """Base Exception class for all Trendr custom exceptions. This gives us an easy way to identify exceptions we raise
    internally as well as a place to add custom behavior to our exceptions like logging/alerting."""

    pass


class ConnectorException(TrendrException):
    """Used when an error is encountered in a connector module."""

    pass
