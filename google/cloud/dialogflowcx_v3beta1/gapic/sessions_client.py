# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Accesses the google.cloud.dialogflow.cx.v3beta1 Sessions API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.cloud.dialogflowcx_v3beta1.gapic import enums
from google.cloud.dialogflowcx_v3beta1.gapic import sessions_client_config
from google.cloud.dialogflowcx_v3beta1.gapic.transports import sessions_grpc_transport
from google.cloud.dialogflowcx_v3beta1.proto import agent_pb2
from google.cloud.dialogflowcx_v3beta1.proto import agent_pb2_grpc
from google.cloud.dialogflowcx_v3beta1.proto import audio_config_pb2
from google.cloud.dialogflowcx_v3beta1.proto import entity_type_pb2
from google.cloud.dialogflowcx_v3beta1.proto import entity_type_pb2_grpc
from google.cloud.dialogflowcx_v3beta1.proto import environment_pb2
from google.cloud.dialogflowcx_v3beta1.proto import environment_pb2_grpc
from google.cloud.dialogflowcx_v3beta1.proto import flow_pb2
from google.cloud.dialogflowcx_v3beta1.proto import flow_pb2_grpc
from google.cloud.dialogflowcx_v3beta1.proto import intent_pb2
from google.cloud.dialogflowcx_v3beta1.proto import intent_pb2_grpc
from google.cloud.dialogflowcx_v3beta1.proto import page_pb2
from google.cloud.dialogflowcx_v3beta1.proto import page_pb2_grpc
from google.cloud.dialogflowcx_v3beta1.proto import session_entity_type_pb2
from google.cloud.dialogflowcx_v3beta1.proto import session_entity_type_pb2_grpc
from google.cloud.dialogflowcx_v3beta1.proto import session_pb2
from google.cloud.dialogflowcx_v3beta1.proto import session_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-dialogflow-cx",
).version


class SessionsClient(object):
    """
    A session represents an interaction with a user. You retrieve user
    input and pass it to the ``DetectIntent`` method to determine user
    intent and respond.
    """

    SERVICE_ADDRESS = "dialogflow.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.dialogflow.cx.v3beta1.Sessions"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SessionsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def session_path(cls, project, location, agent, session):
        """Return a fully-qualified session string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/agents/{agent}/sessions/{session}",
            project=project,
            location=location,
            agent=agent,
            session=session,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.SessionsGrpcTransport,
                    Callable[[~.Credentials, type], ~.SessionsGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = sessions_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=sessions_grpc_transport.SessionsGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = sessions_grpc_transport.SessionsGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials,
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION,
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME],
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def detect_intent(
        self,
        session,
        query_input,
        query_params=None,
        output_audio_config=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Processes a natural language query and returns structured, actionable data
        as a result. This method is not idempotent, because it may cause session
        entity types to be updated, which in turn might affect results of future
        queries.

        Example:
            >>> from google.cloud import dialogflowcx_v3beta1
            >>>
            >>> client = dialogflowcx_v3beta1.SessionsClient()
            >>>
            >>> # TODO: Initialize `session`:
            >>> session = ''
            >>>
            >>> # TODO: Initialize `query_input`:
            >>> query_input = {}
            >>>
            >>> response = client.detect_intent(session, query_input)

        Args:
            session (str): Required. The name of the session this query is sent to. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume default 'draft'
                environment. It's up to the API caller to choose an appropriate
                ``Session ID``. It can be a random number or some type of session
                identifiers (preferably hashed). The length of the ``Session ID`` must
                not exceed 36 characters.

                For more information, see the `sessions
                guide <https://cloud.google.com/dialogflow/cx/docs/concept/session>`__.
            query_input (Union[dict, ~google.cloud.dialogflowcx_v3beta1.types.QueryInput]): Required. The input specification.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflowcx_v3beta1.types.QueryInput`
            query_params (Union[dict, ~google.cloud.dialogflowcx_v3beta1.types.QueryParameters]): The parameters of this query.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflowcx_v3beta1.types.QueryParameters`
            output_audio_config (Union[dict, ~google.cloud.dialogflowcx_v3beta1.types.OutputAudioConfig]): Instructs the speech synthesizer how to generate the output audio.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflowcx_v3beta1.types.OutputAudioConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflowcx_v3beta1.types.DetectIntentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "detect_intent" not in self._inner_api_calls:
            self._inner_api_calls[
                "detect_intent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.detect_intent,
                default_retry=self._method_configs["DetectIntent"].retry,
                default_timeout=self._method_configs["DetectIntent"].timeout,
                client_info=self._client_info,
            )

        request = session_pb2.DetectIntentRequest(
            session=session,
            query_input=query_input,
            query_params=query_params,
            output_audio_config=output_audio_config,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["detect_intent"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def streaming_detect_intent(
        self,
        requests,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Processes a natural language query in audio format in a streaming fashion
        and returns structured, actionable data as a result. This method is only
        available via the gRPC API (not REST).

        Example:
            >>> from google.cloud import dialogflowcx_v3beta1
            >>>
            >>> client = dialogflowcx_v3beta1.SessionsClient()
            >>>
            >>> # TODO: Initialize `query_input`:
            >>> query_input = {}
            >>> request = {'query_input': query_input}
            >>>
            >>> requests = [request]
            >>> for element in client.streaming_detect_intent(requests):
            ...     # process element
            ...     pass

        Args:
            requests (iterator[dict|google.cloud.dialogflowcx_v3beta1.proto.session_pb2.StreamingDetectIntentRequest]): The input objects. If a dict is provided, it must be of the
                same form as the protobuf message :class:`~google.cloud.dialogflowcx_v3beta1.types.StreamingDetectIntentRequest`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.dialogflowcx_v3beta1.types.StreamingDetectIntentResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "streaming_detect_intent" not in self._inner_api_calls:
            self._inner_api_calls[
                "streaming_detect_intent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.streaming_detect_intent,
                default_retry=self._method_configs["StreamingDetectIntent"].retry,
                default_timeout=self._method_configs["StreamingDetectIntent"].timeout,
                client_info=self._client_info,
            )

        return self._inner_api_calls["streaming_detect_intent"](
            requests, retry=retry, timeout=timeout, metadata=metadata
        )

    def match_intent(
        self,
        session,
        query_input,
        query_params=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns preliminary intent match results, doesn't change the session
        status.

        Example:
            >>> from google.cloud import dialogflowcx_v3beta1
            >>>
            >>> client = dialogflowcx_v3beta1.SessionsClient()
            >>>
            >>> # TODO: Initialize `session`:
            >>> session = ''
            >>>
            >>> # TODO: Initialize `query_input`:
            >>> query_input = {}
            >>>
            >>> response = client.match_intent(session, query_input)

        Args:
            session (str): Required. The name of the session this query is sent to. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume default 'draft'
                environment. It's up to the API caller to choose an appropriate
                ``Session ID``. It can be a random number or some type of session
                identifiers (preferably hashed). The length of the ``Session ID`` must
                not exceed 36 characters.

                For more information, see the `sessions
                guide <https://cloud.google.com/dialogflow/cx/docs/concept/session>`__.
            query_input (Union[dict, ~google.cloud.dialogflowcx_v3beta1.types.QueryInput]): Required. The input specification.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflowcx_v3beta1.types.QueryInput`
            query_params (Union[dict, ~google.cloud.dialogflowcx_v3beta1.types.QueryParameters]): The parameters of this query.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflowcx_v3beta1.types.QueryParameters`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflowcx_v3beta1.types.MatchIntentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "match_intent" not in self._inner_api_calls:
            self._inner_api_calls[
                "match_intent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.match_intent,
                default_retry=self._method_configs["MatchIntent"].retry,
                default_timeout=self._method_configs["MatchIntent"].timeout,
                client_info=self._client_info,
            )

        request = session_pb2.MatchIntentRequest(
            session=session, query_input=query_input, query_params=query_params,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session", session)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["match_intent"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def fulfill_intent(
        self,
        match_intent_request=None,
        match=None,
        output_audio_config=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Fulfills a matched intent returned by ``MatchIntent``. Must be
        called after ``MatchIntent``, with input from ``MatchIntentResponse``.
        Otherwise, the behavior is undefined.

        Example:
            >>> from google.cloud import dialogflowcx_v3beta1
            >>>
            >>> client = dialogflowcx_v3beta1.SessionsClient()
            >>>
            >>> response = client.fulfill_intent()

        Args:
            match_intent_request (Union[dict, ~google.cloud.dialogflowcx_v3beta1.types.MatchIntentRequest]): Must be same as the corresponding MatchIntent request, otherwise the
                behavior is undefined.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflowcx_v3beta1.types.MatchIntentRequest`
            match (Union[dict, ~google.cloud.dialogflowcx_v3beta1.types.Match]): The matched intent/event to fulfill.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflowcx_v3beta1.types.Match`
            output_audio_config (Union[dict, ~google.cloud.dialogflowcx_v3beta1.types.OutputAudioConfig]): Instructs the speech synthesizer how to generate output audio.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.dialogflowcx_v3beta1.types.OutputAudioConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.dialogflowcx_v3beta1.types.FulfillIntentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "fulfill_intent" not in self._inner_api_calls:
            self._inner_api_calls[
                "fulfill_intent"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.fulfill_intent,
                default_retry=self._method_configs["FulfillIntent"].retry,
                default_timeout=self._method_configs["FulfillIntent"].timeout,
                client_info=self._client_info,
            )

        request = session_pb2.FulfillIntentRequest(
            match_intent_request=match_intent_request,
            match=match,
            output_audio_config=output_audio_config,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [
                ("match_intent_request.session", match_intent_request.session)
            ]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["fulfill_intent"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )