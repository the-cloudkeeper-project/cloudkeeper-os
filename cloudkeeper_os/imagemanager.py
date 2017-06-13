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
import uuid

import glanceclient.v2.client as glanceclient
from oslo_config import cfg
from oslo_log import log

from cloudkeeper_os import cloudkeeper_pb2
from cloudkeeper_os import keystone_client
from cloudkeeper_os import mapping
from cloudkeeper_os import utils

CONF = cfg.CONF
LOG = log.getLogger(__name__)

APPLIANCE_INT_VALUES = ['ram', 'core', 'expiration_date']
IMAGE_ID_TAG = 'APPLIANCE_ID'
IMAGE_LIST_ID_TAG = 'APPLIANCE_IMAGE_LIST_ID'


class ApplianceManager(object):
    """A class for managing Appliance
    """
    def __init__(self):
        self.mapping = mapping.Mapping()

    def add_appliance(self, appliance):
        """Add an appliance
        """
        project_name = self.mapping.get_project_from_vo(appliance.vo)
        if not project_name:
            # TODO Add a project exception
            LOG.error('No such VO: ' + appliance.vo)
        LOG.debug("Get session for projet: %s" % project_name)
        sess = keystone_client.get_session(project_name=project_name)
        glance = glanceclient.Client(session=sess)
        LOG.info('Adding appliance: ' + appliance.title)
        LOG.debug("Image access mode: "
                  "%s" % appliance.image.Mode.Name(appliance.image.mode))
        if appliance.image.Mode.Name(appliance.image.mode) == 'REMOTE':
            LOG.debug("Downloading image from Cloudkeeper")
            filename = CONF.tempdir + '/' + str(uuid.uuid4())
            kwargs = {}
            kwargs['uri'] = appliance.image.location
            kwargs['filename'] = filename
            kwargs['username'] = appliance.image.username
            kwargs['password'] = appliance.image.password
            if not utils.retrieve_image(**kwargs):
                return None
        else:
            filename = appliance.image.location
        image_format = appliance.image.Format.Name(appliance.image.format)
        appliance.ClearField('image')
        image_data = open(filename, 'rb')
        properties = {}
        for (descriptor, value) in appliance.ListFields():
            if descriptor.name == 'identifier':
                key = IMAGE_ID_TAG
            elif descriptor.name == 'image_list_identifier':
                key = IMAGE_LIST_ID_TAG
            else:
                if descriptor.name == 'attributes':
                    data = dict(value)
                    value = json.dumps(data)
                    LOG.debug("attribute value: %s" % value)
                key = 'APPLIANCE_' + str.upper(descriptor.name)
            properties[key] = str(value)
        # Add property for cloud-info-provider compatibility
        properties['vmcatcher_event_ad_mpuri'] = appliance.mpuri
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
        """Update properties of an appliance
        """
        project_name = self.mapping.get_project_from_vo(appliance.vo)
        sess = keystone_client.get_session(project_name=project_name)
        glance = glanceclient.Client(session=sess)
        filters = {IMAGE_ID_TAG: appliance.identifier,
                   IMAGE_LIST_ID_TAG: appliance.image_list_identifier}
        kwargs = {'filters': filters}
        img_generator = glance.images.list(**kwargs)
        if appliance.HasField('image'):
            appliance.ClearField('image')
        image_list = list(img_generator)
        # TODO Deal the case where a property has been removed
        if len(image_list) > 1:
            LOG.error("Multiple images found with the same properties "
                      "(%s: %s, %s: %s)" % (IMAGE_ID_TAG,
                                            appliance.identifier,
                                            IMAGE_LIST_ID_TAG,
                                            appliance.image_list_identifier))
            return None
        elif len(image_list) == 0:
            LOG.error("No image found with the following properties "
                      "(%s: %s, %s: %s)" % (IMAGE_ID_TAG,
                                            appliance.identifier,
                                            IMAGE_LIST_ID_TAG,
                                            appliance.image_list_identifier))
            return None
        properties = {}
        LOG.info('Updating image: %s' % image_list[0]['id'])
        for (descriptor, value) in appliance.ListFields():
            if descriptor.name == 'identifier':
                key = IMAGE_ID_TAG
            elif descriptor.name == 'image_list_identifier':
                key = IMAGE_LIST_ID_TAG
            else:
                if descriptor.name == 'attributes':
                    data = dict(value)
                    value = json.dumps(data)
                key = 'APPLIANCE_' + str.upper(descriptor.name)
            properties[key] = str(value)
        # Add property for cloud-info-provider compatibility
        properties['vmcatcher_event_ad_mpuri'] = appliance.mpuri
        LOG.debug("Appliance properties updated with new "
                  "values: %s" % (properties))
        glance.images.update(image_list[0]['id'], **properties)

    def remove_appliance(self, appliance):
        """Remove an appliance
        """
        project_name = self.mapping.get_project_from_vo(appliance.vo)
        sess = keystone_client.get_session(project_name=project_name)
        glance = glanceclient.Client(session=sess)
        filters = {IMAGE_ID_TAG: appliance.identifier,
                   IMAGE_LIST_ID_TAG: appliance.image_list_identifier}
        kwargs = {'filters': filters}
        img_generator = glance.images.list(**kwargs)
        image_list = list(img_generator)
        if len(image_list) == 1:
            LOG.info('Deleting image: %s' % image_list[0]['id'])
            glance.images.delete(image_list[0]['id'])
        elif len(image_list) > 1:
            LOG.error("Multiple images found with the same properties "
                      "(%s: %s, %s: %s)" % (IMAGE_ID_TAG,
                                            appliance.identifier,
                                            IMAGE_LIST_ID_TAG,
                                            appliance.image_list_identifier))
        else:
            LOG.error("No image found with the following properties "
                      "(%s: %s, %s: %s)" % (IMAGE_ID_TAG,
                                            appliance.identifier,
                                            IMAGE_LIST_ID_TAG,
                                            appliance.image_list_identifier))


class ImageListManager(object):
    """A class for managing image lists
    """
    def __init__(self):
        """Initialize the ImageListManager
        """
        self.appliances = {}
        self.mapping = mapping.Mapping()

    def update_image_list_identifiers(self, project_name=None):
        """Update the identifier list
        """
        appliances = {}
        if project_name:
            project_list = [project_name]
        else:
            project_list = self.mapping.get_projects()
        for project in project_list:
            try:
                sess = keystone_client.get_session(project)
                glance = glanceclient.Client(session=sess)
                img_generator = glance.images.list()
                image_list = list(img_generator)
                for image in image_list:
                    if IMAGE_LIST_ID_TAG in image:
                        if image[IMAGE_LIST_ID_TAG] not in appliances:
                            appliances[image[IMAGE_LIST_ID_TAG]] = []
                        appliances[image[IMAGE_LIST_ID_TAG]].append(image)
            except Exception:
                LOG.error("Not authorized to manage images from the "
                          "project: %s" % project)
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
            LOG.error("No image with the image_list_identifier: %s" % image_list_identifier)
        vo_name = self.appliances[image_list_identifier][0]['APPLIANCE_VO']
        project_name = self.mapping.get_project_from_vo(vo_name)
        sess = keystone_client.get_session(project_name)
        glance = glanceclient.Client(session=sess)
        for image in self.appliances[image_list_identifier]:
            glance.images.delete(image['id'])
        self.appliances.pop(image_list_identifier)

    def get_image_list_identifiers(self):
        """Return a list of identifiers
        """
        self.update_image_list_identifiers()
        image_list_identifiers = []
        for identifier in self.appliances:
            image_list_identifiers.append(
                cloudkeeper_pb2.ImageListIdentifier(
                    image_list_identifier=identifier
                )
            )
        return image_list_identifiers
