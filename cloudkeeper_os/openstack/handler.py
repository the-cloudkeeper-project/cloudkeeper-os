"""
OpenStack communication handling
"""

from cloudkeeper_os.grpc import cloudkeeper_pb2

from cloudkeeper_os.openstack import glance


class Handler:
    """
    Handler for communication with OpenStack
    """
    def __init__(self):
        self.client = glance.client()

    def register_image(self, request):
        """
        Register image in OpenStack
        """
        image = self.client.images.create(name=request.identifier)

        disk_format = cloudkeeper_pb2._IMAGE_FORMAT.values[request.image.format].name.lower()
        self.client.images.update(image.id, disk_format=disk_format)

        container_format = 'aki'
        self.client.images.update(image.id, container_format=container_format)
        self.client.images.update(image.id, mode=cloudkeeper_pb2._IMAGE_MODE.values[request.image.mode].name)

        self.client.images.upload(image.id, open(request.image.location, 'rb'))

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
