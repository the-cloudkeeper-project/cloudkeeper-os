"""
gRPC method handling
"""
from cloudkeeper_os.grpc import cloudkeeper_pb2_grpc


class CoreConnector(cloudkeeper_pb2_grpc.CommunicatorServicer):
    """
    Implementation of gRPC methods
    """
    def PreAction(self, request, context):  # noqa: N802
        raise NotImplementedError

    def PostAction(self, request, context):  # noqa: N802
        raise NotImplementedError

    def AddAppliance(self, request, context):  # noqa: N802
        raise NotImplementedError

    def UpdateAppliance(self, request, context):  # noqa: N802
        raise NotImplementedError

    def UpdateApplianceMetadata(self, request, context):  # noqa: N802
        raise NotImplementedError

    def RemoveAppliance(self, request, context):  # noqa: N802
        raise NotImplementedError

    def RemoveImageList(self, request, context):  # noqa: N802
        raise NotImplementedError

    def ImageLists(self, request, context):  # noqa: N802
        raise NotImplementedError

    def Appliances(self, request, context):  # noqa: N802
        raise NotImplementedError

    def RemoveExpiredAppliances(self, request, context):  # noqa: N802
        raise NotImplementedError
