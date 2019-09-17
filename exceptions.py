# Custom Exceptions for python modules in Personal-Archiver


class Error(Exception):
    """Base class for other exceptions."""
    pass


class AppleScriptError(Error):
    """Raised when the applescript does not run properly."""
    pass


class DeviceConnectionError(Error):
    """Raised when device is disconnected."""
    pass
