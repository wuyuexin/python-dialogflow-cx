# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.cloud.dialogflow_cx_v3beta1.proto import (
    entity_type_pb2 as google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2,
)
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class EntityTypesStub(object):
    """Service for managing [EntityTypes][google.cloud.dialogflow.cx.v3beta1.EntityType].
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListEntityTypes = channel.unary_unary(
            "/google.cloud.dialogflow.cx.v3beta1.EntityTypes/ListEntityTypes",
            request_serializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.ListEntityTypesRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.ListEntityTypesResponse.FromString,
        )
        self.GetEntityType = channel.unary_unary(
            "/google.cloud.dialogflow.cx.v3beta1.EntityTypes/GetEntityType",
            request_serializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.GetEntityTypeRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.EntityType.FromString,
        )
        self.CreateEntityType = channel.unary_unary(
            "/google.cloud.dialogflow.cx.v3beta1.EntityTypes/CreateEntityType",
            request_serializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.CreateEntityTypeRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.EntityType.FromString,
        )
        self.UpdateEntityType = channel.unary_unary(
            "/google.cloud.dialogflow.cx.v3beta1.EntityTypes/UpdateEntityType",
            request_serializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.UpdateEntityTypeRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.EntityType.FromString,
        )
        self.DeleteEntityType = channel.unary_unary(
            "/google.cloud.dialogflow.cx.v3beta1.EntityTypes/DeleteEntityType",
            request_serializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.DeleteEntityTypeRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class EntityTypesServicer(object):
    """Service for managing [EntityTypes][google.cloud.dialogflow.cx.v3beta1.EntityType].
    """

    def ListEntityTypes(self, request, context):
        """Returns the list of all entity types in the specified agent.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetEntityType(self, request, context):
        """Retrieves the specified entity type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateEntityType(self, request, context):
        """Creates an entity type in the specified agent.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateEntityType(self, request, context):
        """Updates the specified entity type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteEntityType(self, request, context):
        """Deletes the specified entity type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_EntityTypesServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ListEntityTypes": grpc.unary_unary_rpc_method_handler(
            servicer.ListEntityTypes,
            request_deserializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.ListEntityTypesRequest.FromString,
            response_serializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.ListEntityTypesResponse.SerializeToString,
        ),
        "GetEntityType": grpc.unary_unary_rpc_method_handler(
            servicer.GetEntityType,
            request_deserializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.GetEntityTypeRequest.FromString,
            response_serializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.EntityType.SerializeToString,
        ),
        "CreateEntityType": grpc.unary_unary_rpc_method_handler(
            servicer.CreateEntityType,
            request_deserializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.CreateEntityTypeRequest.FromString,
            response_serializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.EntityType.SerializeToString,
        ),
        "UpdateEntityType": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateEntityType,
            request_deserializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.UpdateEntityTypeRequest.FromString,
            response_serializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.EntityType.SerializeToString,
        ),
        "DeleteEntityType": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteEntityType,
            request_deserializer=google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.DeleteEntityTypeRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "google.cloud.dialogflow.cx.v3beta1.EntityTypes", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class EntityTypes(object):
    """Service for managing [EntityTypes][google.cloud.dialogflow.cx.v3beta1.EntityType].
    """

    @staticmethod
    def ListEntityTypes(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.cloud.dialogflow.cx.v3beta1.EntityTypes/ListEntityTypes",
            google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.ListEntityTypesRequest.SerializeToString,
            google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.ListEntityTypesResponse.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetEntityType(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.cloud.dialogflow.cx.v3beta1.EntityTypes/GetEntityType",
            google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.GetEntityTypeRequest.SerializeToString,
            google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.EntityType.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CreateEntityType(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.cloud.dialogflow.cx.v3beta1.EntityTypes/CreateEntityType",
            google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.CreateEntityTypeRequest.SerializeToString,
            google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.EntityType.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UpdateEntityType(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.cloud.dialogflow.cx.v3beta1.EntityTypes/UpdateEntityType",
            google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.UpdateEntityTypeRequest.SerializeToString,
            google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.EntityType.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def DeleteEntityType(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.cloud.dialogflow.cx.v3beta1.EntityTypes/DeleteEntityType",
            google_dot_cloud_dot_dialogflow__cx__v3beta1_dot_proto_dot_entity__type__pb2.DeleteEntityTypeRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )