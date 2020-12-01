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

"""Unit tests."""

import mock
import pytest

from google.cloud import dialogflowcx_v3beta1
from google.cloud.dialogflowcx_v3beta1.proto import intent_pb2
from google.protobuf import empty_pb2


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))

        response = None
        if self.channel_stub.responses:
            response = self.channel_stub.responses.pop()

        if isinstance(response, Exception):
            raise response

        if response:
            return response


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestIntentsClient(object):
    def test_list_intents(self):
        # Setup Expected Response
        next_page_token = ""
        intents_element = {}
        intents = [intents_element]
        expected_response = {"next_page_token": next_page_token, "intents": intents}
        expected_response = intent_pb2.ListIntentsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflowcx_v3beta1.IntentsClient()

        # Setup Request
        parent = client.agent_path("[PROJECT]", "[LOCATION]", "[AGENT]")

        paged_list_response = client.list_intents(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.intents[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = intent_pb2.ListIntentsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_intents_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflowcx_v3beta1.IntentsClient()

        # Setup request
        parent = client.agent_path("[PROJECT]", "[LOCATION]", "[AGENT]")

        paged_list_response = client.list_intents(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_intent(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        priority = 1165461084
        is_fallback = False
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "priority": priority,
            "is_fallback": is_fallback,
        }
        expected_response = intent_pb2.Intent(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflowcx_v3beta1.IntentsClient()

        # Setup Request
        name = client.intent_path("[PROJECT]", "[LOCATION]", "[AGENT]", "[INTENT]")

        response = client.get_intent(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = intent_pb2.GetIntentRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_intent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflowcx_v3beta1.IntentsClient()

        # Setup request
        name = client.intent_path("[PROJECT]", "[LOCATION]", "[AGENT]", "[INTENT]")

        with pytest.raises(CustomException):
            client.get_intent(name)

    def test_create_intent(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        priority = 1165461084
        is_fallback = False
        expected_response = {
            "name": name,
            "display_name": display_name,
            "priority": priority,
            "is_fallback": is_fallback,
        }
        expected_response = intent_pb2.Intent(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflowcx_v3beta1.IntentsClient()

        # Setup Request
        parent = client.agent_path("[PROJECT]", "[LOCATION]", "[AGENT]")
        intent = {}

        response = client.create_intent(parent, intent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = intent_pb2.CreateIntentRequest(parent=parent, intent=intent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_intent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflowcx_v3beta1.IntentsClient()

        # Setup request
        parent = client.agent_path("[PROJECT]", "[LOCATION]", "[AGENT]")
        intent = {}

        with pytest.raises(CustomException):
            client.create_intent(parent, intent)

    def test_update_intent(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        priority = 1165461084
        is_fallback = False
        expected_response = {
            "name": name,
            "display_name": display_name,
            "priority": priority,
            "is_fallback": is_fallback,
        }
        expected_response = intent_pb2.Intent(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflowcx_v3beta1.IntentsClient()

        # Setup Request
        intent = {}

        response = client.update_intent(intent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = intent_pb2.UpdateIntentRequest(intent=intent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_intent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflowcx_v3beta1.IntentsClient()

        # Setup request
        intent = {}

        with pytest.raises(CustomException):
            client.update_intent(intent)

    def test_delete_intent(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflowcx_v3beta1.IntentsClient()

        # Setup Request
        name = client.intent_path("[PROJECT]", "[LOCATION]", "[AGENT]", "[INTENT]")

        client.delete_intent(name)

        assert len(channel.requests) == 1
        expected_request = intent_pb2.DeleteIntentRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_intent_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = dialogflowcx_v3beta1.IntentsClient()

        # Setup request
        name = client.intent_path("[PROJECT]", "[LOCATION]", "[AGENT]", "[INTENT]")

        with pytest.raises(CustomException):
            client.delete_intent(name)