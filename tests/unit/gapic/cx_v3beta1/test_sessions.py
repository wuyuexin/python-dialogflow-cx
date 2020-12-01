# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
#

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.dialogflow.cx_v3beta1.services.sessions import SessionsAsyncClient
from google.cloud.dialogflow.cx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflow.cx_v3beta1.services.sessions import transports
from google.cloud.dialogflow.cx_v3beta1.types import audio_config
from google.cloud.dialogflow.cx_v3beta1.types import entity_type
from google.cloud.dialogflow.cx_v3beta1.types import intent
from google.cloud.dialogflow.cx_v3beta1.types import page
from google.cloud.dialogflow.cx_v3beta1.types import session
from google.cloud.dialogflow.cx_v3beta1.types import session_entity_type
from google.oauth2 import service_account
from google.protobuf import struct_pb2 as struct  # type: ignore
from google.type import latlng_pb2 as latlng  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert SessionsClient._get_default_mtls_endpoint(None) is None
    assert SessionsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        SessionsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SessionsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SessionsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert SessionsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [SessionsClient, SessionsAsyncClient])
def test_sessions_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "dialogflow.googleapis.com:443"


def test_sessions_client_get_transport_class():
    transport = SessionsClient.get_transport_class()
    assert transport == transports.SessionsGrpcTransport

    transport = SessionsClient.get_transport_class("grpc")
    assert transport == transports.SessionsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SessionsClient, transports.SessionsGrpcTransport, "grpc"),
        (SessionsAsyncClient, transports.SessionsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
@mock.patch.object(
    SessionsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SessionsClient)
)
@mock.patch.object(
    SessionsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SessionsAsyncClient),
)
def test_sessions_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(SessionsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(SessionsClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (SessionsClient, transports.SessionsGrpcTransport, "grpc", "true"),
        (
            SessionsAsyncClient,
            transports.SessionsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (SessionsClient, transports.SessionsGrpcTransport, "grpc", "false"),
        (
            SessionsAsyncClient,
            transports.SessionsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    SessionsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SessionsClient)
)
@mock.patch.object(
    SessionsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SessionsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_sessions_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SessionsClient, transports.SessionsGrpcTransport, "grpc"),
        (SessionsAsyncClient, transports.SessionsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_sessions_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SessionsClient, transports.SessionsGrpcTransport, "grpc"),
        (SessionsAsyncClient, transports.SessionsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_sessions_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_sessions_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflow.cx_v3beta1.services.sessions.transports.SessionsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = SessionsClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_detect_intent(
    transport: str = "grpc", request_type=session.DetectIntentRequest
):
    client = SessionsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detect_intent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = session.DetectIntentResponse(
            response_id="response_id_value", output_audio=b"output_audio_blob",
        )

        response = client.detect_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == session.DetectIntentRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, session.DetectIntentResponse)

    assert response.response_id == "response_id_value"

    assert response.output_audio == b"output_audio_blob"


def test_detect_intent_from_dict():
    test_detect_intent(request_type=dict)


@pytest.mark.asyncio
async def test_detect_intent_async(
    transport: str = "grpc_asyncio", request_type=session.DetectIntentRequest
):
    client = SessionsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detect_intent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session.DetectIntentResponse(
                response_id="response_id_value", output_audio=b"output_audio_blob",
            )
        )

        response = await client.detect_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == session.DetectIntentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, session.DetectIntentResponse)

    assert response.response_id == "response_id_value"

    assert response.output_audio == b"output_audio_blob"


@pytest.mark.asyncio
async def test_detect_intent_async_from_dict():
    await test_detect_intent_async(request_type=dict)


def test_detect_intent_field_headers():
    client = SessionsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session.DetectIntentRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detect_intent), "__call__") as call:
        call.return_value = session.DetectIntentResponse()

        client.detect_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_detect_intent_field_headers_async():
    client = SessionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session.DetectIntentRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detect_intent), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session.DetectIntentResponse()
        )

        await client.detect_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_streaming_detect_intent(
    transport: str = "grpc", request_type=session.StreamingDetectIntentRequest
):
    client = SessionsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.streaming_detect_intent), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([session.StreamingDetectIntentResponse()])

        response = client.streaming_detect_intent(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, session.StreamingDetectIntentResponse)


def test_streaming_detect_intent_from_dict():
    test_streaming_detect_intent(request_type=dict)


@pytest.mark.asyncio
async def test_streaming_detect_intent_async(
    transport: str = "grpc_asyncio", request_type=session.StreamingDetectIntentRequest
):
    client = SessionsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.streaming_detect_intent), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[session.StreamingDetectIntentResponse()]
        )

        response = await client.streaming_detect_intent(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, session.StreamingDetectIntentResponse)


@pytest.mark.asyncio
async def test_streaming_detect_intent_async_from_dict():
    await test_streaming_detect_intent_async(request_type=dict)


def test_match_intent(transport: str = "grpc", request_type=session.MatchIntentRequest):
    client = SessionsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.match_intent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = session.MatchIntentResponse(text="text_value",)

        response = client.match_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == session.MatchIntentRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, session.MatchIntentResponse)


def test_match_intent_from_dict():
    test_match_intent(request_type=dict)


@pytest.mark.asyncio
async def test_match_intent_async(
    transport: str = "grpc_asyncio", request_type=session.MatchIntentRequest
):
    client = SessionsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.match_intent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session.MatchIntentResponse()
        )

        response = await client.match_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == session.MatchIntentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, session.MatchIntentResponse)


@pytest.mark.asyncio
async def test_match_intent_async_from_dict():
    await test_match_intent_async(request_type=dict)


def test_match_intent_field_headers():
    client = SessionsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session.MatchIntentRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.match_intent), "__call__") as call:
        call.return_value = session.MatchIntentResponse()

        client.match_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_match_intent_field_headers_async():
    client = SessionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session.MatchIntentRequest()
    request.session = "session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.match_intent), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session.MatchIntentResponse()
        )

        await client.match_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session=session/value",) in kw["metadata"]


def test_fulfill_intent(
    transport: str = "grpc", request_type=session.FulfillIntentRequest
):
    client = SessionsClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fulfill_intent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = session.FulfillIntentResponse(
            response_id="response_id_value", output_audio=b"output_audio_blob",
        )

        response = client.fulfill_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == session.FulfillIntentRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, session.FulfillIntentResponse)

    assert response.response_id == "response_id_value"

    assert response.output_audio == b"output_audio_blob"


def test_fulfill_intent_from_dict():
    test_fulfill_intent(request_type=dict)


@pytest.mark.asyncio
async def test_fulfill_intent_async(
    transport: str = "grpc_asyncio", request_type=session.FulfillIntentRequest
):
    client = SessionsAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fulfill_intent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session.FulfillIntentResponse(
                response_id="response_id_value", output_audio=b"output_audio_blob",
            )
        )

        response = await client.fulfill_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == session.FulfillIntentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, session.FulfillIntentResponse)

    assert response.response_id == "response_id_value"

    assert response.output_audio == b"output_audio_blob"


@pytest.mark.asyncio
async def test_fulfill_intent_async_from_dict():
    await test_fulfill_intent_async(request_type=dict)


def test_fulfill_intent_field_headers():
    client = SessionsClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session.FulfillIntentRequest()
    request.match_intent_request.session = "match_intent_request.session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fulfill_intent), "__call__") as call:
        call.return_value = session.FulfillIntentResponse()

        client.fulfill_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "match_intent_request.session=match_intent_request.session/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_fulfill_intent_field_headers_async():
    client = SessionsAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = session.FulfillIntentRequest()
    request.match_intent_request.session = "match_intent_request.session/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fulfill_intent), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            session.FulfillIntentResponse()
        )

        await client.fulfill_intent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "match_intent_request.session=match_intent_request.session/value",
    ) in kw["metadata"]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SessionsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SessionsClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.SessionsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SessionsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.SessionsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SessionsClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SessionsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = SessionsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SessionsGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.SessionsGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.SessionsGrpcTransport, transports.SessionsGrpcAsyncIOTransport],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = SessionsClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.SessionsGrpcTransport,)


def test_sessions_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.SessionsTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_sessions_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dialogflow.cx_v3beta1.services.sessions.transports.SessionsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.SessionsTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "detect_intent",
        "streaming_detect_intent",
        "match_intent",
        "fulfill_intent",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_sessions_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.dialogflow.cx_v3beta1.services.sessions.transports.SessionsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.SessionsTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


def test_sessions_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.dialogflow.cx_v3beta1.services.sessions.transports.SessionsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.SessionsTransport()
        adc.assert_called_once()


def test_sessions_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        SessionsClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


def test_sessions_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.SessionsGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


def test_sessions_host_no_port():
    client = SessionsClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:443"


def test_sessions_host_with_port():
    client = SessionsClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:8000"


def test_sessions_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.SessionsGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_sessions_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.SessionsGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [transports.SessionsGrpcTransport, transports.SessionsGrpcAsyncIOTransport],
)
def test_sessions_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/dialogflow",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [transports.SessionsGrpcTransport, transports.SessionsGrpcAsyncIOTransport],
)
def test_sessions_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/dialogflow",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_entity_type_path():
    project = "squid"
    location = "clam"
    agent = "whelk"
    entity_type = "octopus"

    expected = "projects/{project}/locations/{location}/agents/{agent}/entityTypes/{entity_type}".format(
        project=project, location=location, agent=agent, entity_type=entity_type,
    )
    actual = SessionsClient.entity_type_path(project, location, agent, entity_type)
    assert expected == actual


def test_parse_entity_type_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "agent": "cuttlefish",
        "entity_type": "mussel",
    }
    path = SessionsClient.entity_type_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_entity_type_path(path)
    assert expected == actual


def test_flow_path():
    project = "winkle"
    location = "nautilus"
    agent = "scallop"
    flow = "abalone"

    expected = "projects/{project}/locations/{location}/agents/{agent}/flows/{flow}".format(
        project=project, location=location, agent=agent, flow=flow,
    )
    actual = SessionsClient.flow_path(project, location, agent, flow)
    assert expected == actual


def test_parse_flow_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "agent": "whelk",
        "flow": "octopus",
    }
    path = SessionsClient.flow_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_flow_path(path)
    assert expected == actual


def test_intent_path():
    project = "oyster"
    location = "nudibranch"
    agent = "cuttlefish"
    intent = "mussel"

    expected = "projects/{project}/locations/{location}/agents/{agent}/intents/{intent}".format(
        project=project, location=location, agent=agent, intent=intent,
    )
    actual = SessionsClient.intent_path(project, location, agent, intent)
    assert expected == actual


def test_parse_intent_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "agent": "scallop",
        "intent": "abalone",
    }
    path = SessionsClient.intent_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_intent_path(path)
    assert expected == actual


def test_page_path():
    project = "squid"
    location = "clam"
    agent = "whelk"
    flow = "octopus"
    page = "oyster"

    expected = "projects/{project}/locations/{location}/agents/{agent}/flows/{flow}/pages/{page}".format(
        project=project, location=location, agent=agent, flow=flow, page=page,
    )
    actual = SessionsClient.page_path(project, location, agent, flow, page)
    assert expected == actual


def test_parse_page_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "agent": "mussel",
        "flow": "winkle",
        "page": "nautilus",
    }
    path = SessionsClient.page_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_page_path(path)
    assert expected == actual


def test_session_path():
    project = "scallop"
    location = "abalone"
    agent = "squid"
    session = "clam"

    expected = "projects/{project}/locations/{location}/agents/{agent}/sessions/{session}".format(
        project=project, location=location, agent=agent, session=session,
    )
    actual = SessionsClient.session_path(project, location, agent, session)
    assert expected == actual


def test_parse_session_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
        "agent": "oyster",
        "session": "nudibranch",
    }
    path = SessionsClient.session_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_session_path(path)
    assert expected == actual


def test_session_entity_type_path():
    project = "cuttlefish"
    location = "mussel"
    agent = "winkle"
    session = "nautilus"
    entity_type = "scallop"

    expected = "projects/{project}/locations/{location}/agents/{agent}/sessions/{session}/entityTypes/{entity_type}".format(
        project=project,
        location=location,
        agent=agent,
        session=session,
        entity_type=entity_type,
    )
    actual = SessionsClient.session_entity_type_path(
        project, location, agent, session, entity_type
    )
    assert expected == actual


def test_parse_session_entity_type_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "agent": "clam",
        "session": "whelk",
        "entity_type": "octopus",
    }
    path = SessionsClient.session_entity_type_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_session_entity_type_path(path)
    assert expected == actual


def test_transition_route_group_path():
    project = "oyster"
    location = "nudibranch"
    agent = "cuttlefish"
    flow = "mussel"
    transition_route_group = "winkle"

    expected = "projects/{project}/locations/{location}/agents/{agent}/flows/{flow}/transitionRouteGroups/{transition_route_group}".format(
        project=project,
        location=location,
        agent=agent,
        flow=flow,
        transition_route_group=transition_route_group,
    )
    actual = SessionsClient.transition_route_group_path(
        project, location, agent, flow, transition_route_group
    )
    assert expected == actual


def test_parse_transition_route_group_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "agent": "abalone",
        "flow": "squid",
        "transition_route_group": "clam",
    }
    path = SessionsClient.transition_route_group_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_transition_route_group_path(path)
    assert expected == actual


def test_webhook_path():
    project = "whelk"
    location = "octopus"
    agent = "oyster"
    webhook = "nudibranch"

    expected = "projects/{project}/locations/{location}/agents/{agent}/webhooks/{webhook}".format(
        project=project, location=location, agent=agent, webhook=webhook,
    )
    actual = SessionsClient.webhook_path(project, location, agent, webhook)
    assert expected == actual


def test_parse_webhook_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "agent": "winkle",
        "webhook": "nautilus",
    }
    path = SessionsClient.webhook_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_webhook_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = SessionsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = SessionsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"

    expected = "folders/{folder}".format(folder=folder,)
    actual = SessionsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = SessionsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = SessionsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = SessionsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"

    expected = "projects/{project}".format(project=project,)
    actual = SessionsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = SessionsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = SessionsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = SessionsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = SessionsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.SessionsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = SessionsClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.SessionsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = SessionsClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
