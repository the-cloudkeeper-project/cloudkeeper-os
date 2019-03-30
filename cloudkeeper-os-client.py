# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc

from cloudkeeper_os.grpc import cloudkeeper_pb2
from cloudkeeper_os.grpc import cloudkeeper_pb2_grpc

from oslo_config import cfg


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        # channel = grpc.insecure_channel('localhost:50051')
        stub = cloudkeeper_pb2_grpc.CommunicatorStub(channel)
        response = stub.AddAppliance(cloudkeeper_pb2.Appliance(identifier='TestImage',
                                                                title='simulated_image',
                                                                description='simulated image for testing',
                                                                mpuri='',
                                                                group='group1',
                                                                ram=3,
                                                                core=4,
                                                                version='v2',
                                                                architecture='architecture1',
                                                                operating_system='OpenSuse',
                                                                vo='vo1',
                                                                expiration_date=24032021,
                                                                image_list_identifier='55',
                                                                base_mpuri='',
                                                                appid='15',
                                                                digest='digest',
                                                                image=cloudkeeper_pb2.Image(
                                                                        mode=cloudkeeper_pb2.Image.REMOTE,
                                                                        format=cloudkeeper_pb2.Image.RAW,
                                                                        location='/tmp/myimage.iso',
                                                                        digest='SHA',
                                                                                        uri='uri/uri',
                                                                                        checksum='checksumvalue',
                                                                                        size=512,
                                                                                        username='demo',
                                                                                        password='openstack',
                                                                                        )
                                                                )
                                        )

        print("Greeter client received: " + str(response))

if __name__ == '__main__':
    logging.basicConfig()
    run()
