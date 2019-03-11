"""
Exceptions specific for communication with OpenStack
"""


from cloudkeeper_os.exceptions import CloudkeeperOSException


class UnknownAuthMethod(CloudkeeperOSException):
    """
    Thrown when trying to request unsupported authentication method
    """
