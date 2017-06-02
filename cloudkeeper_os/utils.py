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

def retrieve_image(uri, filename, username=None, password=None, capath=None):
    """Retrieve an image
    """
    # TODO manage SSL case
    if username and password:
        auth = HTTPBasicAuth(username, password)
        response = requests.get(uri, auth=auth, stream=True)
    else:
        response = requests.get(uri, stream=True)
    if response.status_code == 200:
        output = open(filename, 'wb')
        # response.raw.decode_content = True
        shutil.copyfileobj(response.raw, output)
        output.close()
