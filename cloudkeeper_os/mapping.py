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

"""A set of tools for manipulating voms mapping file
"""

import json

from oslo_config import cfg
from oslo_log import log

CONF = cfg.CONF

LOG = log.getLogger(__name__)

class Mapping(object):
    """An object for managing the VO / project mapping
    """
    def __init__(self):
        self.vo_mapping = {}
        self.project_mapping = {}
        try:
            mapping = json.loads(open(CONF.mapping_file).read())
            for (vo_name, details) in mapping.items():
                self.vo_mapping[vo_name] = details['tenant']
                self.project_mapping[details['tenant']] = vo_name
        except IOError:
            LOG.error("Failed to open mapping file.")

    def get_project_from_vo(self, vo_name):
        """Return the project associated to the VO
        """
        if vo_name in self.vo_mapping:
            return self.vo_mapping[vo_name]
        else:
            return None

    def get_vo_from_project(self, project):
        """Return the VO associated to the project
        """
        if project in self.project_mapping:
            return self.project_mapping[project]
        else:
            return None

    def get_vos(self):
        """Return the list of supported VOs
        """
        return self.vo_mapping.keys()

    def get_projects(self):
        """Return the list of VO-related project
        """
        return self.project_mapping.keys()
