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

<<<<<<< Updated upstream
    def set_tags(self):
=======
        params = {}

        if request.title:
            params[self.APPLIANCE_TAGS_PREFIX + 'title'] = request.title
            params['name'] = request.title
        if request.description:
            params[self.APPLIANCE_TAGS_PREFIX + 'description'] = request.description
            params['description'] = request.description
        if request.mpuri:
            params[self.APPLIANCE_TAGS_PREFIX + 'mpuri'] = request.mpuri
        if request.group:
            params[self.APPLIANCE_TAGS_PREFIX + 'group'] = request.group
        if request.ram:
            params[self.APPLIANCE_TAGS_PREFIX + 'ram'] = str(request.ram)
            params['min_ram'] = request.ram
        if request.core:
            params[self.APPLIANCE_TAGS_PREFIX + 'core'] = str(request.core)
            params['min_disk'] = request.core
        if request.version:
            params[self.APPLIANCE_TAGS_PREFIX + 'version'] = request.version
        if request.architecture:
            params[self.APPLIANCE_TAGS_PREFIX + 'architecture'] = request.architecture
        if request.operating_system:
            params[self.APPLIANCE_TAGS_PREFIX + 'operating_system'] = request.operating_system
        if request.vo:
            params[self.APPLIANCE_TAGS_PREFIX + 'vo'] = request.vo
        if request.expiration_date:
            params[self.APPLIANCE_TAGS_PREFIX + 'expiration_date'] = str(request.expiration_date)
        if request.image_list_identifier:
            params[self.APPLIANCE_TAGS_PREFIX + 'image_list_identifier'] = request.image_list_identifier
        if request.base_mpuri:
            params[self.APPLIANCE_TAGS_PREFIX + 'base_mpuri'] = request.base_mpuri
        if request.appid:
            params[self.APPLIANCE_TAGS_PREFIX + 'appid'] = request.appid
        if request.digest:
            params[self.APPLIANCE_TAGS_PREFIX + 'digest'] = request.digest

        return params

    def image_dict_to_appliance_message(self, request):
        appliance_dict = {}
        
        for k, v in request.items():
            if self.APPLIANCE_TAGS_PREFIX in k:
                if k.replace(self.APPLIANCE_TAGS_PREFIX, '') == 'expiration_date':
                    appliance_dict[k.replace(self.APPLIANCE_TAGS_PREFIX, '')] = int(v)
                else:
                    appliance_dict[k.replace(self.APPLIANCE_TAGS_PREFIX, '')] = v

        if 'id' in request:
            appliance_dict['identifier'] = request['id']
        if 'name' in request:
            appliance_dict['title'] = request['name']
        if 'description' in request:
            appliance_dict['description'] = request['description']
        if 'min_ram' in request:
            appliance_dict['ram'] = int(request['min_ram'])
        if 'min_disk' in request:
            appliance_dict['core'] = int(request['min_disk'])

        image_dict = {}


        if 'os_hash_algo' in request:
            image_dict['digest'] = request['os_hash_algo']
        if 'size' in request:
            image_dict['size'] = request['size']
        if 'checksum' in request:
            image_dict['checksum'] = request['checksum']
        if 'container_format' in request:
            try:
                image_dict['container_format'] = cloudkeeper_pb2.Image.Format.Value(request['container_format'].upper())
            except:
                pass
        if 'disk_format' in request:
            try:
                image_dict['format'] = cloudkeeper_pb2.Image.Format.Value(request['disk_format'].upper())
            except:
                pass

        return([appliance_dict, image_dict])

    def get_appliance(self, appliance_id):
>>>>>>> Stashed changes
        """
        Set metadata for image
        """
        raise NotImplementedError

    def update_tags(self):
        """
        Update metadata for image
        """
        raise NotImplementedError

<<<<<<< Updated upstream
    def delete_image(self):
=======
        name = request.operating_system + '-' + request.version + '-' + request.architecture
        appliance = self.client.images.create(name=name)

        self.register_image(request.image, appliance.id)

        params = self.appliance_metadata_to_dict(request)

        self.update_tags(appliance.id, **params)

    def register_image(self, request, image_id):
>>>>>>> Stashed changes
        """
        Delete image from OpenStack
        """
<<<<<<< Updated upstream
        raise NotImplementedError
=======

        format = cloudkeeper_pb2.Image.Format.Name(request.format).lower()
        image = self.client.images.update(image_id, disk_format=format)

        container_format = cloudkeeper_pb2.Image.Format.Name(request.container_format).lower()
        image = self.client.images.update(image_id, container_format=container_format)

        if (request.mode == cloudkeeper_pb2.Image.LOCAL):
            image = self.client.images.upload(image_id, open(request.location, 'rb'))
        elif (request.mode == cloudkeeper_pb2.Image.REMOTE):
            self.client.images.image_import(image_id, method='web-download', uri=request.uri)

    def update_image(self, request, appliance_id):
        """
        Update image in Appliance
        """

        old_appliance = self.get_appliance(appliance_id)

        new_appliance_list = self.image_dict_to_appliance_message(old_appliance)

        self.remove_appliance(appliance_id)

        self.register_appliance(cloudkeeper_pb2.Appliance(**new_appliance_list[0], image=request))

    def update_tags(self, appliance_id, **params):
        """
        Update metadata for Appliance
        """

        image = self.client.images.update(appliance_id, **params)

        return image

    def remove_appliance(self, appliance_id):
        """
        Delete appliance from OpenStack
        """

        image = self.client.images.delete(appliance_id)
>>>>>>> Stashed changes

    def list_images(self):
        """
        List images from OpenStack
        """
<<<<<<< Updated upstream
        raise NotImplementedError
=======
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
>>>>>>> Stashed changes
