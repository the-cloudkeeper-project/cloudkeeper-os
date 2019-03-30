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

    def register_appliance(self, request):
        """
        Register appliance in OpenStack
        """

        name = request.operating_system + '-' + request.version + '-' + request.architecture
        appliance = self.client.images.create(name=name)

        self.register_image(request.image, appliance.id)

        params = {
            'description': request.description,
            'mpuri': request.mpuri,
            'group': request.group,
            'min_ram': request.ram,
            'min_disk': request.core,
            'version': request.version,
            'architecture': request.architecture,
            'operating_system': request.operating_system,
            'vo': request.vo,
            'expiration_date': str(request.expiration_date),
            'image_list_identifier': request.image_list_identifier,
            'base_mpuri': request.base_mpuri,
            'appid': request.appid
        }

        self.client.images.update(appliance.id, **params)

    def register_image(self, request, image_id):
        """
        Register image in OpenStack
        """
        disk_format = cloudkeeper_pb2._IMAGE_FORMAT.values[request.format].name.lower()
        image = self.client.images.update(image_id, disk_format=disk_format)

        container_format = 'aki'
        image = self.client.images.update(image_id, container_format=container_format)

        mode = cloudkeeper_pb2._IMAGE_MODE.values[request.mode].name
        image = self.client.images.update(image_id, mode=mode)

        image = self.client.images.upload(image_id, open(request.location, 'rb'))

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
