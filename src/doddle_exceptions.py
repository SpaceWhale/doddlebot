"""
:author: john.sosoka
:date: 5/10/2018

Collection of custom doddle exceptions.
"""


class DirectoryCreateException(Exception):
    """
    Raised when the client is unable to build a directory of slack channels.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CommandParseException(Exception):
    """
    Raised when the output from the slack rtm api cannot be parsed
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PluginPrepareException(Exception):
    """
    Raised when the application is unable to build a list of plugin candidates
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ConfigOptionRetrievalException(Exception):
    """
    Raised when a config option cannot be retrieved.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
