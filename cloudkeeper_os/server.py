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
from cloudkeeper_os import keystone_client

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

LOG = log.getLogger(__name__)

class CommunicatorServicer(cloudkeeper_pb2_grpc.CommunicatorServicer):
    """Provides methods that implement functionnality of cloudkeeper server.
    """
    def PreAction(self, request, context):
        pass

    def PostAction(self, request, context):
        pass

    def AddAppliance(self, request, context):
        """params: Appliance
           returns: google.protobuf.Empty
        """
        vo = request.vo
        #add project_from_vo function
        session = keystone_client.get_session(vo)
        #glance.create_image(session=session, name=image_name,
        #                    disk_format=image_format,
        #                    container_format=container_format,
        #                    data=fimage, properties=properties_dict
        #                   )

    def UpdateAppliance(self, request, context):
        """params: Appliance
           returns: google.protobuf.Empty
        """
        pass

    def RemoveAppliance(self, request, context):
        """params: Appliance
           returns: google.protobuf.Empty
        """
        pass

    def RemoveImageList(self, request, context):
        """params: ImageListIdentifier
           returns: google.protobuf.Empty
        """
        pass

    def ImageLists(self, request, context):
        """params: empty
           returns: ImageListIdentifier
        """
        image_list = cloudkeeper_pb2.ImageListIdentifier()
        return image_list

    def Appliances(self, request, context):
        """params: ImageListIdentifier
           returns: Appliance
        """
        appliance = cloudkeeper_pb2.Appliance()
        return appliance

def serve():
    """Configure and launch the service
    """
    try:
        config.parse_args(sys.argv)
        #log.setup(cfg.CONF, 'cloudkeeper-os')
        #log.set_defaults()
        #config.set_config_defaults()
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
