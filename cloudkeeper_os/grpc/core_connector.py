"""
gRPC method handling
"""
from cloudkeeper_os.grpc import cloudkeeper_pb2_grpc


class CoreConnector(cloudkeeper_pb2_grpc.CommunicatorServicer):
    """
    Implementation of gRPC methods
    """
<<<<<<< Updated upstream
=======

    def __init__(self):
        super().__init__()
        self.LOG = log.getLogger(__name__)
        self.h = handler.Handler()

>>>>>>> Stashed changes
    def PreAction(self, request, context):  # noqa: N802
        pass

        return cloudkeeper_pb2.Empty()

    def PostAction(self, request, context):  # noqa: N802
        pass

<<<<<<< Updated upstream
    def AddAppliance(self, request, context):  # noqa: N802
        raise NotImplementedError

    def UpdateAppliance(self, request, context):  # noqa: N802
        raise NotImplementedError

    def UpdateApplianceMetadata(self, request, context):  # noqa: N802
        raise NotImplementedError

    def RemoveAppliance(self, request, context):  # noqa: N802
        raise NotImplementedError
=======
        return cloudkeeper_pb2.Empty()

    def AddAppliance(self, request, context):  # noqa: N802
        self.h.register_appliance(request)

        return cloudkeeper_pb2.Empty()

    def UpdateAppliance(self, request, context):  # noqa: N802
        self.UpdateApplianceMetadata(request, context)
        self.h.update_image(request.image, request.identifier)

        return cloudkeeper_pb2.Empty()

    def UpdateApplianceMetadata(self, request, context):  # noqa: N802
        params = self.h.appliance_metadata_to_dict(request)
        image = self.h.update_tags(request.identifier, **params)

        return cloudkeeper_pb2.Empty()

    def RemoveAppliance(self, request, context):  # noqa: N802
        self.h.remove_appliance(request.identifier)

        return cloudkeeper_pb2.Empty()
>>>>>>> Stashed changes

    def RemoveImageList(self, request, context):  # noqa: N802
        pass

        return cloudkeeper_pb2.Empty()

    def ImageLists(self, request, context):  # noqa: N802
        pass

        yield cloudkeeper_pb2.Empty()

    def Appliances(self, request, context):  # noqa: N802
<<<<<<< Updated upstream
        raise NotImplementedError

    def RemoveExpiredAppliances(self, request, context):  # noqa: N802
        raise NotImplementedError
=======
        images = self.h.list_images()
        for i in images:
            appliance_image_list = self.h.image_dict_to_appliance_message(i)
            appliance_dict = appliance_image_list[0]
            appliance_dict['image'] = cloudkeeper_pb2.Image(**appliance_image_list[1])

            yield cloudkeeper_pb2.Appliance(**appliance_dict)

    def RemoveExpiredAppliances(self, request, context):  # noqa: N802
        self.h.remove_expired_appliances()

        return cloudkeeper_pb2.Empty()
>>>>>>> Stashed changes
