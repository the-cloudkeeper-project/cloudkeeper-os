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

from cloudkeeper_os import cloudkeeper_pb2_grpc
from cloudkeeper_os import cloudkeeper_pb2
from cloudkeeper_os import config
from cloudkeeper_os import imagemanager

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

LOG = log.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "cloudkeeper-os"


class CommunicatorServicer(cloudkeeper_pb2_grpc.CommunicatorServicer):
    """Provides methods that implement functionnality of cloudkeeper server.
    """
    def PreAction(self, request, context):
        metadata = (
            ('status', 'SUCCESS'),
        )
        LOG.debug("Sending metadata information ('%s': '%s')" % metadata[0])
        context.set_trailing_metadata(metadata)
        return cloudkeeper_pb2.Empty()

    def PostAction(self, request, context):
        """Cleanup of images marked for removal
        """
        LOG.info("Cleaning up appliances marked for removal")
        manager = imagemanager.ApplianceManager()
        manager.cleanup_appliances()
        metadata = (
            ('status', 'SUCCESS'),
        )
        LOG.debug("Sending metadata information ('%s': '%s')" % metadata[0])
        context.set_trailing_metadata(metadata)
        return cloudkeeper_pb2.Empty()

    def AddAppliance(self, request, context):
        """params: Appliance
           returns: google.protobuf.Empty
        """
        metadata = (
            ('status', 'SUCCESS'),
        )
        LOG.info("Adding appliance: %s" % request.identifier)
        manager = imagemanager.ApplianceManager()
        if not manager.add_appliance(request):
            metadata = (
                ('status', 'ERROR'),
            )
        LOG.debug("Sending metadata information ('%s': '%s')" % metadata[0])
        context.set_trailing_metadata(metadata)
        return cloudkeeper_pb2.Empty()

    def UpdateAppliance(self, request, context):
        """params: Appliance
           returns: google.protobuf.Empty
        """
        metadata = (
            ('status', 'SUCCESS'),
        )
        LOG.info("updating appliance: %s" % request.identifier)
        manager = imagemanager.ApplianceManager()
        if not manager.update_appliance(request):
            metadata = (
                ('status', 'ERROR'),
            )
        LOG.debug("Sending metadata information ('%s': '%s')" % metadata[0])
        context.set_trailing_metadata(metadata)
        return cloudkeeper_pb2.Empty()

    def RemoveAppliance(self, request, context):
        """params: Appliance
           returns: google.protobuf.Empty
        """
        metadata = (
            ('status', 'SUCCESS'),
        )
        LOG.info("Marking appliances for removal: %s" % request.identifier)
        manager = imagemanager.ApplianceManager()
        if not manager.mark_appliance_for_removal(request):
            metadata = (
                ('status', 'ERROR'),
            )
        LOG.debug("Sending metadata information ('%s': '%s')" % metadata[0])
        context.set_trailing_metadata(metadata)
        return cloudkeeper_pb2.Empty()

    def RemoveImageList(self, request, context):
        """params: ImageListIdentifier
           returns: google.protobuf.Empty
        """
        metadata = (
            ('status', 'SUCCESS'),
        )
        LOG.info("Removing image list identifier "
                 "identifier: %s" % request.image_list_identifier)
        manager = imagemanager.ImageListManager()
        manager.remove_image_list(request.image_list_identifier)
        LOG.debug("Sending metadata information ('%s': '%s')" % metadata[0])
        context.set_trailing_metadata(metadata)
        return cloudkeeper_pb2.Empty()

    def ImageLists(self, request, context):
        """params: empty
           returns: ImageListIdentifier
        """
        metadata = (
            ('status', 'SUCCESS'),
        )
        manager = imagemanager.ImageListManager()
        for image_list_identifier in manager.get_image_list_identifiers():
            yield image_list_identifier
        LOG.debug("Sending metadata information ('%s': '%s')" % metadata[0])
        context.set_trailing_metadata(metadata)

    def Appliances(self, request, context):
        """params: ImageListIdentifier
           returns: Appliance
        """
        metadata = (
            ('status', 'SUCCESS'),
        )
        manager = imagemanager.ImageListManager()
        for appliance in manager.get_appliances(request.image_list_identifier):
            yield appliance
        LOG.debug("Sending metadata information ('%s': '%s')" % metadata[0])
        context.set_trailing_metadata(metadata)


def serve():
    """Configure and launch the service
    """
    log.register_options(CONF)
    log.set_defaults()
    try:
        config.parse_args(sys.argv)
        log.setup(CONF, DOMAIN)
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
