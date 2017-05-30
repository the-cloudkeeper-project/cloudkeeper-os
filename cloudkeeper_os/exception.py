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

"""CloudKeeper exception subclasses"""

from oslo_log import log
import six

LOG = log.getLogger(__name__)

@six.python_2_unicode_compatible
class CloudkeeperException(Exception):
    """Base Cloudkeeper Exception.

    To correctly use this class, inherit from it and define a 'message'
    property. That message will get printf'd with the keyword arguments
    provided to the constructor.
    """
    message = "An unknown exception occured."
    code = 500

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs and hasattr(self, 'code'):
            self.kwargs['code'] = self.code

        if message:
            self.message = message

        try:
            self.message = self.message % kwargs
        except KeyError:
            # kwargs doesn't match a variable in the message
            # log the issue and the kwargs
            LOG.exception('Exception in string format operation, '
                          'kwargs: %s' % kwargs)
        super(CloudkeeperException, self).__init__(self.message)

    def __str__(self):
        return self.message

    def __unicode__(self):
        return self.message


class ProjectNotFound(CloudkeeperException):
    """Cloudkeeper exception raised when a project is not found.
    """
    message = "Project %(project_name)s could not be found."

