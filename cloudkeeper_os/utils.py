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

"""A set of utils for Cloudkeeper-OS
"""

import json
import math
import shutil
import uuid

import requests
from requests.auth import HTTPBasicAuth

from oslo_config import cfg
from oslo_log import log

from cloudkeeper_os import constants

CONF = cfg.CONF
LOG = log.getLogger(__name__)
IMAGE_ID_TAG = constants.IMAGE_ID_TAG
IMAGE_LIST_ID_TAG = constants.IMAGE_LIST_ID_TAG


def retrieve_image(appliance):
    """Retrieve an image from Cloudkeeper NGINX
    """
    # TODO manage SSL case
    filename = CONF.tempdir + '/' + str(uuid.uuid4())
    uri = appliance.image.location
    username = appliance.image.username
    password = appliance.image.password

    LOG.info("Download image from %s" % uri)
    auth = HTTPBasicAuth(username, password)
    response = requests.get(uri, auth=auth, stream=True)
    LOG.debug("Response: %s when accessing the "
              "image." % str(response.status_code))
    if response.status_code == 200:
        output = open(filename, 'wb')
        shutil.copyfileobj(response.raw, output)
        output.close()
        LOG.debug("Image data successfully saved to %s" % filename)
    else:
        LOG.error("Failed to download image data due to HTTP error")
        return None
    return filename


def find_images(glance_client, identifier, image_list_identifier):
    """Search for glance images given a appliance and image list identifiers
    """
    # Check that identifier and image_list_identifier are not too small
    if len(identifier) <= 3:
        LOG.error('The identifier %s is too small' % identifier)
        return None
    if len(image_list_identifier) <= 3:
        LOG.error("The image_list_identifier %s is too "
                  "small" % image_list_identifier)
        return None
    filters = {IMAGE_ID_TAG: identifier,
               IMAGE_LIST_ID_TAG: image_list_identifier}
    kwargs = {'filters': filters}
    img_generator = glance_client.images.list(**kwargs)
    image_list = list(img_generator)
    if len(image_list) == 0:
        LOG.error("No image found with the following properties "
                  "(%s: %s, %s: %s)" % (IMAGE_ID_TAG, identifier,
                                        IMAGE_LIST_ID_TAG,
                                        image_list_identifier))
        return None
    else:
        return image_list


def extract_appliance_properties(appliance):
    """Extract properties from an appliance
    """
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
    return properties


def convert_ram(ram_value):
    """Convert ram in bytes to the nearest upper integer in megabytes
    """
    return int(math.ceil(ram_value/1048576))
