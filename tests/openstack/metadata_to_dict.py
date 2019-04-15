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

from cloudkeeper_os.grpc.cloudkeeper_grpc_python import cloudkeeper_pb2
from cloudkeeper_os.grpc.cloudkeeper_grpc_python import cloudkeeper_pb2_grpc
from cloudkeeper_os.openstack import handler

from oslo_config import cfg

def test():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        # channel = grpc.insecure_channel('localhost:50051')
        stub = cloudkeeper_pb2_grpc.CommunicatorStub(channel)
        response = stub.AddAppliance(cloudkeeper_pb2.Appliance(identifier='2a5451eb-91f3-46a2-95a7-9cff7362d553',
                                                                title='simulated_image',
                                                                description='simulated image for testing',
                                                                mpuri='',
                                                                group='group1',
                                                                ram=2048,
                                                                core=4,
                                                                version='0.0.5867',
                                                                architecture='x86_64',
                                                                operating_system='OpenSuse',
                                                                vo='some.dummy.vo',
                                                                expiration_date=1556582400,
                                                                image_list_identifier='76fdee70-8119-5d33-aaaa-3c57e1c60df1',
                                                                base_mpuri='',
                                                                appid='993',
                                                                digest='digest',
                                                                image=cloudkeeper_pb2.Image(
                                                                        # mode=cloudkeeper_pb2.Image.REMOTE,
                                                                        format=cloudkeeper_pb2.Image.RAW,
                                                                        container_format=cloudkeeper_pb2.Image.AKI,
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
    test()