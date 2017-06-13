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

import shutil

import requests
from requests.auth import HTTPBasicAuth

from oslo_log import log

LOG = log.getLogger(__name__)

def retrieve_image(uri, filename, username='', password='', capath=None):
    """Retrieve an image
    """
    # TODO manage SSL case
    LOG.info("Download image from %s" % uri)
    auth = HTTPBasicAuth(username, password)
    response = requests.get(uri, auth=auth, stream=True)
    LOG.debug("Response: %s when accessing the image." % str(response.status_code))
    if response.status_code == 200:
        output = open(filename, 'wb')
        shutil.copyfileobj(response.raw, output)
        output.close()
        LOG.debug("Image data successfully saved to %s" % filename)
        return True
    else:
        # TODO raise an exception
        LOG.error("Failed to download image data due to HTTP error")
        return False
