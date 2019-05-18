"""
gRPC method handling
"""

from oslo_log import log

from cloudkeeper_os.grpc.cloudkeeper_grpc_python import cloudkeeper_pb2
from cloudkeeper_os.grpc.cloudkeeper_grpc_python import cloudkeeper_pb2_grpc

from cloudkeeper_os.openstack import handler

class CoreConnector(cloudkeeper_pb2_grpc.CommunicatorServicer):
    """
    Implementation of gRPC methods
    """

    def __init__(self):
        super().__init__()
        self.LOG = log.getLogger(__name__)

    def PreAction(self, request, context):  # noqa: N802
        raise NotImplementedError

    def PostAction(self, request, context):  # noqa: N802
        raise NotImplementedError

    def AddAppliance(self, request, context):  # noqa: N802
        h = handler.Handler()
        h.register_appliance(request)
        return cloudkeeper_pb2.Empty()

    def UpdateAppliance(self, request, context):  # noqa: N802
        h = handler.Handler()

        h.register_image(request.image, request.identifier)

        image = self.UpdateApplianceMetadata(request)

        return cloudkeeper_pb2.Empty()

    def UpdateApplianceMetadata(self, request, context):  # noqa: N802
        h = handler.Handler()
        params = h.appliance_metadata_to_dict(request)
        image = h.update_tags(request.identifier, **params)
        return cloudkeeper_pb2.Empty()

    def RemoveAppliance(self, request, context):  # noqa: N802
        h = handler.Handler()
        h.remove_appliance(request.identifier)
        return cloudkeeper_pb2.Empty()

    def RemoveImageList(self, request, context):  # noqa: N802
        raise NotImplementedError

    def ImageLists(self, request, context):  # noqa: N802
        raise NotImplementedError

    def Appliances(self, request, context):  # noqa: N802
        h = handler.Handler()
        images = h.list_images()
        for i in images:
            print('\n')
            appliance_image_list = h.image_dict_to_appliance_message(i)

            appliance_dict = appliance_image_list[0]
            appliance_dict['image'] = cloudkeeper_pb2.Image(**appliance_image_list[1])
            yield cloudkeeper_pb2.Appliance(**appliance_dict)

    def RemoveExpiredAppliances(self, request, context):  # noqa: N802
        h = handler.Handler()

        h.remove_expired_appliances(request)

        return cloudkeeper_pb2.Empty()
