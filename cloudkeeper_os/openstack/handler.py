"""
OpenStack communication handling
"""


from cloudkeeper_os.openstack import glance


class Handler:
    """
    Handler for communication with OpenStack
    """
    def __init__(self):
        self.client = glance.client()

    def register_image(self):
        """
        Register image in OpenStack
        """
        raise NotImplementedError

    def set_tags(self):
        """
        Set metadata for image
        """
        raise NotImplementedError

    def update_tags(self):
        """
        Update metadata for image
        """
        raise NotImplementedError

    def delete_image(self):
        """
        Delete image from OpenStack
        """
        raise NotImplementedError

    def list_images(self):
        """
        List images from OpenStack
        """
        raise NotImplementedError
