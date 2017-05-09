# -*- coding: utf-8 -*-

# Copyright 2017 CNRS and University of Strasbourg
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Image Manager
"""

import glanceclient.v2.client as glanceclient
from oslo_log import log

from cloudkeeper_os import keystone_client
from cloudkeeper_os import mapping

LOG = log.getLogger(__name__)

IMAGE_LIST_ID_TAG = 'image_list_identifier'

class ImageManager(object):
    """A class for managing images
    """
    def __init__(self):
        """Initialize the ImageListManager
        """
        self.identifiers = {}
        self.images = {}
        self.mapping = mapping.Mapping()

    def update_image_list_identifiers(self, project=None):
        """Update the identifier list
        """
        if project:
            project_list = [project]
        else:
            project_list = self.mapping.get_projects()
        for project in project_list:
            sess = keystone_client.get_session(project)
            glance = glanceclient.Client(session=sess)
            img_generator = glance.images.list()
            for image in img_generator:
                if IMAGE_LIST_ID_TAG in image:
                    if image[IMAGE_LIST_ID_TAG] not in self.identifiers:
                        self.identifiers[image[IMAGE_LIST_ID_TAG]] = project
                        self.images[image[IMAGE_LIST_ID_TAG]] = {}
                    self.images[image[IMAGE_LIST_ID_TAG]][image.id] = image

    def add_appliance(self, appliance):
        """Add an appliance
        """
        project_name = self.mapping.get_project_from_vo(appliance.vo)
        sess = keystone_client.get_session(project_name=project_name)
        glance = glanceclient.Client(session=sess)
        LOG.info('Adding appliance: ' + appliance.title)
        image_data = open(appliance.image, 'r')
        properties = {}
        glance.images.create(session=sess, name=appliance.title,
                             data=image_data, properties=properties
                            )

    def update_appliance(self, appliance):
        """Update an appliance
        """
        project_name = self.mapping.get_project_from_vo(appliance.vo)
        sess = keystone_client.get_session(project_name=project_name)
        glance = glanceclient.Client(session=sess)
        filters = {'ck_identifier' : appliance.identifier}
        kwargs = {'filters': filters}
        img_generator = glance.images.list(**kwargs)
        image_list = []
        for image in img_generator.next():
            image_list.append(image)
        # Add a check on the number of images. Should be one.

    def remove_appliance(self, appliance):
        """Remove an appliance
        """
        project_name = self.mapping.get_project_from_vo(appliance.vo)
        sess = keystone_client.get_session(project_name=project_name)
        glance = glanceclient.Client(session=sess)
        filters = {'ck_identifier' : appliance.identifier}
        kwargs = {'filters': filters}
        img_generator = glance.images.list(**kwargs)
        image_list = []
        for image in img_generator.next():
            image_list.append(image)
        # Add a check on the number of images. Should be one.
        LOG.info('Deleting appliance: ' + image_list[0]['id'])
        glance.images.delete(image_list[0]['id'])

    def remove_image_list(self, image_list_identifier):
        """Remove all images linked to an image_list_identifier
        """
        pass

    def get_image_list_identifiers(self):
        """Return a list of identifiers
        """
        return self.identifiers.keys()

    def get_appliances(self, image_list_identifier):
        """Return all appliances with a given image_list_identifier
        """
        self.update_image_list_identifiers()
        return self.images[image_list_identifier]
