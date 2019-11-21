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
import random
import string

import grpc

from cloudkeeper_os.grpc.cloudkeeper_grpc_python import cloudkeeper_pb2
from cloudkeeper_os.grpc.cloudkeeper_grpc_python import cloudkeeper_pb2_grpc

from oslo_config import cfg

def gen_rand_name():
    """
    Generate random name for Appliance
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(30))

def if_name_in_list(gen_name, appliances_names):
    """
    Check if Appliance Name is already in list
    """
    if gen_name in appliances_names:
        return True
    else:
        return False

def get_appliances_titles_list(stub):

    try:
        appliances_names = []
        for feature in stub.Appliances(cloudkeeper_pb2.ImageListIdentifier()):
            appliances_names.append(feature.title)
    except Exception as err:
        print('Error while getting appliances using Appliances method \n\n Error: ' + str(err))
        exit()

    return appliances_names

def get_appliance(stub, gen_name):

    try:
        appliance = {}
        for feature in stub.Appliances(cloudkeeper_pb2.ImageListIdentifier()):
            if str(feature.title) == str(gen_name):
                appliance = feature

    except Exception as err:
        print('Error while getting appliances using Appliances method \n\n Error: ' + str(err))
        exit()

    return appliance

Image_dict = {
                'mode': cloudkeeper_pb2.Image.LOCAL,
                'format': cloudkeeper_pb2.Image.RAW,
                'container_format': cloudkeeper_pb2.Image.BARE,
                'location': 'tests/demo_images/cirros-0.4.0-x86_64-disk.img',
                'digest': 'SHA',
                'uri': 'https://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img',
                'checksum': 'checksumvalue',
                'size': 512,
                'username': 'demo',
                'password': 'openstack'

                }

Appliance_dict = {
                    'description': 'testing_image',
                    'mpuri': '',
                    'group': 'group1',
                    'ram': 2048,
                    'core': 4,
                    'version': '0.0.5867',
                    'architecture': 'x86_64',
                    'operating_system': 'OpenSuse',
                    'vo': 'some.dummy.vo',
                    'expiration_date': 1556582400,
                    'image_list_identifier': '76fdee70-8119-5d33-aaaa-3c57e1c60df1',
                    'base_mpuri': '',
                    'appid': '993',
                    'digest': 'digest',
                    'image': cloudkeeper_pb2.Image(**Image_dict)

                    }

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        # channel = grpc.insecure_channel('localhost:50051')
        stub = cloudkeeper_pb2_grpc.CommunicatorStub(channel)
        
        #TODO: finish Appliances method in core_connector, so it could use find()

        name_in_list = True

        while name_in_list:
            gen_name = gen_rand_name()
            appliances_names = get_appliances_titles_list(stub)
            name_in_list = if_name_in_list(gen_name, appliances_names)

        print('Using name for testing: ' + str(gen_name))

        try:
            new_appliance = stub.AddAppliance(cloudkeeper_pb2.Appliance(**Appliance_dict, title=str(gen_name)))
            print(new_appliance)
        except Exception as err:
            print('Error while creating appliance using AddAppliance method \n\n Error: ' + str(err))
            exit()

        appliances_names = get_appliances_titles_list(stub)
        name_in_list = if_name_in_list(gen_name, appliances_names)

        if name_in_list:
            print('Added')
        else:
            print('Error: Your AddAppliance method doesn\'t work well... Appliance wasn\'t added')

        print('Description of appliance: ' + str(get_appliance(stub, gen_name).description))

        try:
            new_appliance = stub.UpdateApplianceMetadata(cloudkeeper_pb2.Appliance(identifier=str(get_appliance(stub, gen_name).identifier), description='updated_testing_image'))
        except Exception as err:
            print('Error while updating appliance using UpdateApplianceMetadata method \n\n Error: ' + str(err))
            exit()

        if str(get_appliance(stub, gen_name).description) == 'updated_testing_image':
            print('Updated, Description of appliance: ' + str(get_appliance(stub, gen_name).description))
        else:
            print('Error: Your UpdateApplianceMetadata method doesn\'t work well... Appliance wasn\'t updated')

        # print('Container of image: ' + str(get_appliance(stub, gen_name).cloudkeeper_pb2.Image.Format.Value))

        Image_dict['container_format'] = cloudkeeper_pb2.Image.BARE

        try:
            new_appliance = stub.UpdateAppliance(cloudkeeper_pb2.Appliance(identifier=str(get_appliance(stub, gen_name).identifier), 
                                                                            image=cloudkeeper_pb2.Image(**Image_dict)))
        except Exception as err:
            print('Error while updating image using UpdateAppliance method \n\n Error: ' + str(err))
            exit()

        if get_appliance(stub, gen_name).image.container_format == cloudkeeper_pb2.Image.BARE:
            print('Updated, Size of Image: ' + str(get_appliance(stub, gen_name).image.size))
        else:
            print('Error: Your UpdateAppliance method doesn\'t work well... Image wasn\'t updated')
        

        try:
            new_appliance = stub.RemoveAppliance(cloudkeeper_pb2.Appliance(identifier=str(get_appliance(stub, gen_name).identifier)))
        except Exception as err:
            print('Error while removing appliance using RemoveAppliance method \n\n Error: ' + str(err))
            exit()

        appliances_names = get_appliances_titles_list(stub)
        name_in_list = if_name_in_list(gen_name, appliances_names)

        if name_in_list:
            print('Error: Your RemoveAppliance method doesn\'t work well... Appliance wasn\'t removed')
            print('!!! DON\'T FORGET TO REMOVE TESTING APPLIANCE MANUALLY !!!')
        else:
            print('Removed')
        

        # response = stub.AddAppliance(cloudkeeper_pb2.Appliance(**Appliance_dict, title=)
        # response = stub.RemoveAppliance(cloudkeeper_pb2.Appliance(identifier='10c8551c-4b0e-403d-8421-fa240fd9bc0f', title='asd'))
        
        # pprint(response)

if __name__ == '__main__':
    logging.basicConfig()
    run()

# print(gen_rand_name())
