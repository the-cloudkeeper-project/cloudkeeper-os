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

import json

from oslo_config import cfg
from oslo_log import log

from cloudkeeper_os import cloudkeeper_pb2
from cloudkeeper_os import constants
from cloudkeeper_os import openstack_client
from cloudkeeper_os import mapping
from cloudkeeper_os import utils

CONF = cfg.CONF
LOG = log.getLogger(__name__)
IMAGE_ID_TAG = constants.IMAGE_ID_TAG
IMAGE_LIST_ID_TAG = constants.IMAGE_LIST_ID_TAG
APPLIANCE_INT_VALUES = constants.APPLIANCE_INT_VALUES


class ApplianceManager(object):
    """A class for managing Appliance
    """
    def __init__(self):
        self.mapping = mapping.Mapping()


    def add_appliance(self, appliance):
        """Add an appliance to glance
        """
        project_name = self.mapping.get_project_from_vo(appliance.vo)
        if not project_name:
            LOG.debug("Cannot get project name from vo %s" % appliance.vo)
            return None

        glance = openstack_client.get_glance_client(project_name)
        if not glance:
            LOG.error("Cannot get glance client for project %s" % project_name)
            return None

        LOG.info('Adding appliance: ' + appliance.title)

        LOG.debug("Image access mode: "
                  "%s" % appliance.image.Mode.Name(appliance.image.mode))
        if appliance.image.Mode.Name(appliance.image.mode) == 'REMOTE':
            filename = utils.retrieve_image(appliance)
        else:
            filename = appliance.image.location
        if not filename:
            LOG.error("Image filename is not set.")
            return None
        image_format = appliance.image.Format.Name(appliance.image.format)
        try:
            image_data = open(filename, 'rb')
        except IOError as err:
            LOG.error("Can not open image file: %s" % filename)
            LOG.exception(err)
            return None
        appliance.ClearField('image')

        properties = utils.extract_appliance_properties(appliance)

        LOG.debug("Create image %s (format: %s, "
                  "properties %s)" % (appliance.title,
                                      str.lower(image_format),
                                      properties)
                 )

        glance_image = glance.images.create(name=appliance.title,
                                            disk_format=str.lower(image_format),
                                            container_format="bare"
                                           )
        glance.images.upload(glance_image.id, image_data)
        glance.images.update(glance_image.id, **properties)
        return glance_image.id

    def update_appliance(self, appliance):
        """Update an appliance stored in glance
        """
        project_name = self.mapping.get_project_from_vo(appliance.vo)
        if not project_name:
            LOG.debug("Cannot get project name from vo %s" % appliance.vo)
            return None

        glance = openstack_client.get_glance_client(project_name)
        if not glance:
            LOG.error("Cannot get glance client for project %s" % project_name)
            return None

        glance_image = utils.find_image(glance, appliance.identifier,
                                        appliance.image_list_identifier)
        if not glance_image:
            LOG.info('Cannot delete image: image not found')
            return None

        LOG.debug("Image access mode: "
                  "%s" % appliance.image.Mode.Name(appliance.image.mode))
        if appliance.image.Mode.Name(appliance.image.mode) == 'REMOTE':
            filename = utils.retrieve_image(appliance)
        else:
            filename = appliance.image.location
        if not filename:
            LOG.error("Image filename is not set.")
            return None
        image_format = appliance.image.Format.Name(appliance.image.format)
        try:
            image_data = open(filename, 'rb')
        except IOError as err:
            LOG.error("Can not open image file: %s" % filename)
            LOG.exception(err)
            return None
        appliance.ClearField('image')

        properties = utils.extract_appliance_properties(appliance)
        properties['disk_format'] = str.lower(image_format)

        LOG.info('Updating image: %s' % glance_image.id)
        LOG.debug("Appliance properties updated with new "
                  "values: %s" % (properties))
        glance.images.upload(glance_image.id, image_data)
        glance.images.update(glance_image.id, **properties)
        return glance_image.id


    def remove_appliance(self, appliance):
        """Remove an appliance in glance
        """
        project_name = self.mapping.get_project_from_vo(appliance.vo)
        if not project_name:
            LOG.debug("Cannot get project name from vo %s" % appliance.vo)
            return None

        glance = openstack_client.get_glance_client(project_name)
        if not glance:
            LOG.error("Cannot get glance client for project %s" % project_name)
            return None

        glance_image = utils.find_image(glance, appliance.identifier,
                                        appliance.image_list_identifier)
        if not glance_image:
            LOG.info('Cannot delete image: image not found')
            return None

        LOG.info('Deleting image: %s' % glance_image.id)
        return glance_image.id


class ImageListManager(object):
    """A class for managing image lists
    """
    def __init__(self):
        """Initialize the ImageListManager
        """
        self.appliances = {}
        self.mapping = mapping.Mapping()

    def update_image_list_identifiers(self):
        """Update the identifier list
        """
        appliances = {}

        for project_name in self.mapping.get_projects():
            glance = openstack_client.get_glance_client(project_name)
            if not glance:
                LOG.error("Not authorized to manage images from the "
                          "project: %s" % project_name)
                continue
            try:
                img_generator = glance.images.list()
                image_list = list(img_generator)
            except Exception:
                LOG.error("Not authorized to manage images from the "
                          "project: %s" % project_name)
                continue

            for image in image_list:
                if IMAGE_LIST_ID_TAG in image:
                    if image[IMAGE_LIST_ID_TAG] not in appliances:
                        appliances[image[IMAGE_LIST_ID_TAG]] = []
                    appliances[image[IMAGE_LIST_ID_TAG]].append(image)

        self.appliances = appliances

    def get_appliances(self, image_list_identifier):
        """Return all appliances with a given image_list_identifier
        """
        self.update_image_list_identifiers()
        appliance_list = []
        for image in self.appliances[image_list_identifier]:
            properties = {}
            for field in cloudkeeper_pb2.Appliance.DESCRIPTOR.fields_by_name:
                if field == 'identifier':
                    key = IMAGE_ID_TAG
                elif field == 'image_list_identifier':
                    key = IMAGE_LIST_ID_TAG
                else:
                    key = 'APPLIANCE_'+str.upper(field)
                if key in image:
                    if field in APPLIANCE_INT_VALUES:
                        properties[field] = long(image[key])
                    elif field == 'attributes':
                        properties[field] = json.loads(image[key])
                    else:
                        properties[field] = image[key]
            LOG.debug(image)
            LOG.debug('properties: %s' % properties)
            appliance_list.append(
                cloudkeeper_pb2.Appliance(**properties)
            )
        return appliance_list

    def remove_image_list(self, image_list_identifier):
        """Remove all images linked to an image_list_identifier
        """
        self.update_image_list_identifiers()
        if image_list_identifier not in self.appliances:
            # raise NotIdentifierFound exception
            LOG.error("No image with the image_list_identifier:"
                      "%s" % image_list_identifier)
            return None
        vo_name = self.appliances[image_list_identifier][0]['APPLIANCE_VO']
        project_name = self.mapping.get_project_from_vo(vo_name)
        if not project_name:
            LOG.debug("Cannot get project name from vo %s" % vo_name)
            return None

        glance = openstack_client.get_glance_client(project_name)
        if not glance:
            LOG.error("Cannot get glance client for project %s" % project_name)
            return None

        LOG.debug("Delete all images with the Image List Identifier: "
                  "%s" % image_list_identifier)
        for image in self.appliances[image_list_identifier]:
            LOG.info("Deleting image %s" % image['id'])
            glance.images.delete(image['id'])
        self.appliances.pop(image_list_identifier)
        return image_list_identifier

    def get_image_list_identifiers(self):
        """Return a list of identifiers
        """
        self.update_image_list_identifiers()
        image_list_identifiers = []
        for identifier in self.appliances:
            LOG.debug("Append new image list identifier: %s" % identifier)
            image_list_identifiers.append(
                cloudkeeper_pb2.ImageListIdentifier(
                    image_list_identifier=identifier
                )
            )
        return image_list_identifiers
