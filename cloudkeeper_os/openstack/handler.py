"""
OpenStack communication handling
"""
import time

from cloudkeeper_os.grpc.cloudkeeper_grpc_python import cloudkeeper_pb2

from cloudkeeper_os.openstack import glance


class Handler:
    """
    Handler for communication with OpenStack
    """
    def __init__(self):
        self.client = glance.client()

    def appliance_metadata_to_dict(self, request):
        """
        Parsing Appliance metadata to dictionary
        """

        APPLIANCE_TAGS_PREFIX = 'CLOUDKEEPER_'
        params = {}

        if request.title:
            params[APPLIANCE_TAGS_PREFIX + 'title'] = request.title
        if request.description:
            params[APPLIANCE_TAGS_PREFIX + 'description'] = request.description
            params['description'] = request.description
        if request.mpuri:
            params[APPLIANCE_TAGS_PREFIX + 'mpuri'] = request.mpuri
        if request.group:
            params[APPLIANCE_TAGS_PREFIX + 'group'] = request.group
        if request.ram:
            params[APPLIANCE_TAGS_PREFIX + 'ram'] = str(request.ram)
            params['min_ram'] = request.ram
        if request.core:
            params[APPLIANCE_TAGS_PREFIX + 'core'] = str(request.core)
            params['min_disk'] = request.core
        if request.version:
            params[APPLIANCE_TAGS_PREFIX + 'version'] = request.version
        if request.architecture:
            params[APPLIANCE_TAGS_PREFIX + 'architecture'] = request.architecture
        if request.operating_system:
            params[APPLIANCE_TAGS_PREFIX + 'operating_system'] = request.operating_system
        if request.vo:
            params[APPLIANCE_TAGS_PREFIX + 'vo'] = request.vo
        if request.expiration_date:
            params[APPLIANCE_TAGS_PREFIX + 'expiration_date'] = str(request.expiration_date)
        if request.image_list_identifier:
            params[APPLIANCE_TAGS_PREFIX + 'image_list_identifier'] = request.image_list_identifier
        if request.base_mpuri:
            params[APPLIANCE_TAGS_PREFIX + 'base_mpuri'] = request.base_mpuri
        if request.appid:
            params[APPLIANCE_TAGS_PREFIX + 'appid'] = request.appid

        return params

    def get_appliance(self, appliance_id):
        """
        Getting appliance from Openstack
        """

        appliance = self.client.images.get(appliance_id)
        return appliance

    def register_appliance(self, request):
        """
        Register appliance in OpenStack
        """

        name = request.operating_system + '-' + request.version + '-' + request.architecture
        appliance = self.client.images.create(name=name)

        self.register_image(request.image, appliance.id)

        params = self.appliance_metadata_to_dict(request)

        self.update_tags(appliance.id, **params)

    def register_image(self, request, image_id):
        """
        Upload image in Openstack
        """

        disk_format = cloudkeeper_pb2._IMAGE_FORMAT.values[request.format].name.lower()
        image = self.client.images.update(image_id, disk_format=disk_format)

        container_format = 'aki'
        image = self.client.images.update(image_id, container_format=container_format)

        mode = cloudkeeper_pb2._IMAGE_MODE.values[request.mode].name
        image = self.client.images.update(image_id, mode=mode)

        image = self.client.images.upload(image_id, open(request.location, 'rb'))

    def update_tags(self, appliance_id, **params):
        """
        Update metadata for Appliance
        """

        self.client.images.update(appliance_id, **params)

    def remove_appliance(self, appliance_id):
        """
        Delete appliance from OpenStack
        """

        self.client.images.delete(appliance_id)

    def list_images(self):
        """
        List images from OpenStack
        """
        image_list = self.client.images.list()

        return image_list

    def remove_expired_appliances(self):
        """
        Remove expired appliances from OpenStack
        """

        image_list = self.list_images()
        current_time = time.time()

        for image in image_list:
            if 'CLOUDKEEPER_expiration_date' in image:
                if int(image['CLOUDKEEPER_expiration_date']) < current_time:
                    self.remove_appliance(image['id'])
