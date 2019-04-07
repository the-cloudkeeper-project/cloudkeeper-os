"""
gRPC method handling
"""

from cloudkeeper_os.grpc.cloudkeeper_grpc_python import cloudkeeper_pb2
from cloudkeeper_os.grpc.cloudkeeper_grpc_python import cloudkeeper_pb2_grpc

from cloudkeeper_os.openstack import handler

class CoreConnector(cloudkeeper_pb2_grpc.CommunicatorServicer):
    """
    Implementation of gRPC methods
    """
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

        self.UpdateApplianceMetadata(request, context)

        if request.image:
            h.register_image(request.image, request.identifier)
        else:
            return cloudkeeper_pb2.Empty()

    def UpdateApplianceMetadata(self, request, context):  # noqa: N802
        h = handler.Handler()
        params = h.appliance_metadata_to_dict(request)
        h.update_tags(request.identifier, **params)
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
        return cloudkeeper_pb2.Empty()

    def RemoveExpiredAppliances(self, request, context):  # noqa: N802
        h = handler.Handler()

        h.remove_expired_appliances(request)

        return cloudkeeper_pb2.Empty()
