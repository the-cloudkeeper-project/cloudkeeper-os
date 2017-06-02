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

"""Cloudkeeper-os Server.

This implements the OpenStack backend for the Cloudkeeper software.
"""

import sys
import time

from concurrent import futures
import grpc
from oslo_log import log
from oslo_config import cfg

from cloudkeeper_os import cloudkeeper_pb2
from cloudkeeper_os import cloudkeeper_pb2_grpc
from cloudkeeper_os import config
from cloudkeeper_os import imagemanager

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

LOG = log.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "cloudkeeper-os"

class CommunicatorServicer(cloudkeeper_pb2_grpc.CommunicatorServicer):
    """Provides methods that implement functionnality of cloudkeeper server.
    """
    def __init__(self):
        pass

    def PreAction(self, request, context):
        return cloudkeeper_pb2.Empty()

    def PostAction(self, request, context):
        return cloudkeeper_pb2.Empty()

    def AddAppliance(self, request, context):
        """params: Appliance
           returns: google.protobuf.Empty
        """
        LOG.info("Adding appliance: %s" % request.identifier)
        manager = imagemanager.ApplianceManager()
        manager.add_appliance(request)
        return cloudkeeper_pb2.Empty()

    def UpdateAppliance(self, request, context):
        """params: Appliance
           returns: google.protobuf.Empty
        """
        LOG.info("updating appliance: %s" % request.identifier)
        manager = imagemanager.ApplianceManager()
        manager.update_appliance(request)
        return cloudkeeper_pb2.Empty()

    def RemoveAppliance(self, request, context):
        """params: Appliance
           returns: google.protobuf.Empty
        """
        LOG.info("Removing appliance: %s" % request.identifier)
        manager = imagemanager.ApplianceManager()
        manager.remove_appliance(request)
        return cloudkeeper_pb2.Empty()

    def RemoveImageList(self, request, context):
        """params: ImageListIdentifier
           returns: google.protobuf.Empty
        """
        LOG.info("Removing image list identifier: %s" % request.image_list_identifier)
        manager = imagemanager.ImageListManager()
        manager.remove_image_list(request.image_list_identifier)
        return cloudkeeper_pb2.Empty()

    def ImageLists(self, request, context):
        """params: empty
           returns: ImageListIdentifier
        """
        manager = imagemanager.ImageListManager()
        for image_list_identifier in manager.get_image_list_identifiers():
            yield image_list_identifier

    def Appliances(self, request, context):
        """params: ImageListIdentifier
           returns: Appliance
        """
        manager = imagemanager.ImageListManager()
        for appliance in manager.get_appliances(request.image_list_identifier):
            yield appliance


def serve():
    """Configure and launch the service
    """
    log.register_options(CONF)
    log.setup(CONF, DOMAIN)
    try:
        config.parse_args(sys.argv)
    except RuntimeError as rtex:
        LOG.exception(rtex)
        sys.exit(1)
    grpc_port = cfg.CONF.grpc_port
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cloudkeeper_pb2_grpc.add_CommunicatorServicer_to_server(
        CommunicatorServicer(), server)
    server.add_insecure_port('[::]:' + str(grpc_port))
    LOG.info('Starting Cloudkeeper-OS on port: %i' % grpc_port)

    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
