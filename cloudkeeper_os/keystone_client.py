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

"""Keystone helper
"""

from keystoneauth1.identity import v3
from keystoneauth1 import session
from oslo_config import cfg

CONF = cfg.CONF

CFG_GROUP = "keystone_authtoken"

def get_session(project_name):
    """Get an auth session.
    """
    auth_params = dict(CONF[CFG_GROUP])
    auth_params['project_name'] = project_name
    auth = v3.Password(**auth_params)
    return session.Session(auth=auth, verify=False)
