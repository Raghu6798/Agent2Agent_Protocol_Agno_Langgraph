import asyncio
import base64
import os
import urllib
import httpx

import traceback
from uuid import uuid4
import time

import asyncclick as click
from jwt import PyJWK, PyJWKClient
import jwt
import json
import hashlib
from typing import Any

from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    Part,
    TextPart,
    FilePart,
    FileWithBytes,
    Task,
    TaskState,
    Message,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
    MessageSendConfiguration,
    SendMessageRequest,
    SendStreamingMessageRequest,
    MessageSendParams,
    GetTaskRequest,
    TaskQueryParams,
    JSONRPCErrorResponse,
)

import threading
from starlette.responses import Response
from starlette.applications import Starlette
from starlette.requests import Request
AUTH_HEADER_PREFIX = 'Bearer '


class PushNotificationAuth:
    def _calculate_request_body_sha256(self, data: dict[str, Any]):
        """Calculates the SHA256 hash of a request body.

        This logic needs to be same for both the agent who signs the payload and the client verifier.
        """
        body_str = json.dumps(
            data,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(',', ':'),
        )
        return hashlib.sha256(body_str.encode()).hexdigest()
class PushNotificationReceiverAuth(PushNotificationAuth):
    def __init__(self):
        self.public_keys_jwks = []
        self.jwks_client = None

    async def load_jwks(self, jwks_url: str):
        self.jwks_client = PyJWKClient(jwks_url)

    async def verify_push_notification(self, request: Request) -> bool:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith(AUTH_HEADER_PREFIX):
            print('Invalid authorization header')
            return False

        token = auth_header[len(AUTH_HEADER_PREFIX) :]
        signing_key = self.jwks_client.get_signing_key_from_jwt(token)

        decode_token = jwt.decode(
            token,
            signing_key,
            options={'require': ['iat', 'request_body_sha256']},
            algorithms=['RS256'],
        )

        actual_body_sha256 = self._calculate_request_body_sha256(
            await request.json()
        )
        if actual_body_sha256 != decode_token['request_body_sha256']:
            # Payload signature does not match the digest in signed token.
            raise ValueError('Invalid request body')

        if time.time() - decode_token['iat'] > 60 * 5:
            # Do not allow push-notifications older than 5 minutes.
            # This is to prevent replay attack.
            raise ValueError('Token is expired')

        return True


class PushNotificationListener:
    def __init__(
        self,
        host,
        port,
        notification_receiver_auth: PushNotificationReceiverAuth,
    ):
        self.host = host
        self.port = port
        self.notification_receiver_auth = notification_receiver_auth
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(
            target=lambda loop: loop.run_forever(), args=(self.loop,)
        )
        self.thread.daemon = True
        self.thread.start()

    def start(self):
        try:
            # Need to start server in separate thread as current thread
            # will be blocked when it is waiting on user prompt.
            asyncio.run_coroutine_threadsafe(
                self.start_server(),
                self.loop,
            )
            print('======= push notification listener started =======')
        except Exception as e:
            print(e)

    async def start_server(self):
        import uvicorn

        self.app = Starlette()
        self.app.add_route(
            '/notify', self.handle_notification, methods=['POST']
        )
        self.app.add_route(
            '/notify', self.handle_validation_check, methods=['GET']
        )

        config = uvicorn.Config(
            self.app, host=self.host, port=self.port, log_level='critical'
        )
        self.server = uvicorn.Server(config)
        await self.server.serve()

    async def handle_validation_check(self, request: Request):
        validation_token = request.query_params.get('validationToken')
        print(
            f'\npush notification verification received => \n{validation_token}\n'
        )

        if not validation_token:
            return Response(status_code=400)

        return Response(content=validation_token, status_code=200)

    async def handle_notification(self, request: Request):
        data = await request.json()
        try:
            if not await self.notification_receiver_auth.verify_push_notification(
                request
            ):
                print('push notification verification failed')
                return
        except Exception as e:
            print(f'error verifying push notification: {e}')
            print(traceback.format_exc())
            return

        print(f'\npush notification received => \n{data}\n')
        return Response(status_code=200)

class PushNotificationAuth:
    def _calculate_request_body_sha256(self, data: dict[str, Any]):
        """Calculates the SHA256 hash of a request body.

        This logic needs to be same for both the agent who signs the payload and the client verifier.
        """
        body_str = json.dumps(
            data,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(',', ':'),
        )
        return hashlib.sha256(body_str.encode()).hexdigest()
class PushNotificationReceiverAuth(PushNotificationAuth):
    def __init__(self):
        self.public_keys_jwks = []
        self.jwks_client = None

    async def load_jwks(self, jwks_url: str):
        self.jwks_client = PyJWKClient(jwks_url)

    async def verify_push_notification(self, request: Request) -> bool:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith(AUTH_HEADER_PREFIX):
            print('Invalid authorization header')
            return False

        token = auth_header[len(AUTH_HEADER_PREFIX) :]
        signing_key = self.jwks_client.get_signing_key_from_jwt(token)

        decode_token = jwt.decode(
            token,
            signing_key,
            options={'require': ['iat', 'request_body_sha256']},
            algorithms=['RS256'],
        )

        actual_body_sha256 = self._calculate_request_body_sha256(
            await request.json()
        )
        if actual_body_sha256 != decode_token['request_body_sha256']:
            # Payload signature does not match the digest in signed token.
            raise ValueError('Invalid request body')

        if time.time() - decode_token['iat'] > 60 * 5:
            # Do not allow push-notifications older than 5 minutes.
            # This is to prevent replay attack.
            raise ValueError('Token is expired')

        return True


@click.command()
@click.option('--agent', default='http://localhost:10000')
@click.option('--session', default=0)
@click.option('--history', default=False)
@click.option('--use_push_notifications', default=False)
@click.option('--push_notification_receiver', default='http://localhost:5000')
async def cli(
    agent,
    session,
    history,
    use_push_notifications: bool,
    push_notification_receiver: str,
):
    async with httpx.AsyncClient(timeout=30) as httpx_client:
        card_resolver = A2ACardResolver(httpx_client, agent)
        card = await card_resolver.get_agent_card()

        print('======= Agent Card ========')
        print(card.model_dump_json(exclude_none=True))

        notif_receiver_parsed = urllib.parse.urlparse(
            push_notification_receiver)
        notification_receiver_host = notif_receiver_parsed.hostname
        notification_receiver_port = notif_receiver_parsed.port

        if use_push_notifications:
           

            notification_receiver_auth = PushNotificationReceiverAuth()
            await notification_receiver_auth.load_jwks(
                f'{agent}/.well-known/jwks.json'
            )

            push_notification_listener = PushNotificationListener(
                host=notification_receiver_host,
                port=notification_receiver_port,
                notification_receiver_auth=notification_receiver_auth,
            )
            push_notification_listener.start()

        client = A2AClient(httpx_client, agent_card=card)

        continue_loop = True
        streaming = card.capabilities.streaming

        while continue_loop:
            print('=========  starting a new task ======== ')
            continue_loop, contextId, taskId = await completeTask(
                client,
                streaming,
                use_push_notifications,
                notification_receiver_host,
                notification_receiver_port,
                None,
                None,
            )

            if history and continue_loop:
                print('========= history ======== ')
                task_response = await client.get_task(
                    GetTaskRequest(
                        id=str(uuid4()),
                        params=TaskQueryParams(id=taskId, historyLength=10)
                    )
                )
                print(
                    task_response.model_dump_json(
                        include={'result': {'history': True}}
                    )
                )


async def completeTask(
    client: A2AClient,
    streaming,
    use_push_notifications: bool,
    notification_receiver_host: str,
    notification_receiver_port: int,
    taskId,
    contextId,
):
    prompt = click.prompt(
        '\nWhat do you want to send to the agent? (:q or quit to exit)'
    )
    if prompt == ':q' or prompt == 'quit':
        return False, None, None

    message = Message(
        role='user',
        parts=[TextPart(text=prompt)],
        messageId=str(uuid4()),
        taskId=taskId,
        contextId=contextId,
    )

    file_path = click.prompt(
        'Select a file path to attach? (press enter to skip)',
        default='',
        show_default=False,
    )
    if file_path and file_path.strip() != '':
        with open(file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode('utf-8')
            file_name = os.path.basename(file_path)

        message.parts.append(
            Part(
                root=FilePart(
                    file=FileWithBytes(
                        name=file_name, bytes=file_content
                    )
                )
            )
        )

    payload = MessageSendParams(
        id=str(uuid4()),
        message=message,
        configuration=MessageSendConfiguration(
            acceptedOutputModes=['text'],
        ),
    )

    if use_push_notifications:
        payload['pushNotification'] = {
            'url': f'http://{notification_receiver_host}:{notification_receiver_port}/notify',
            'authentication': {
                'schemes': ['bearer'],
            },
        }

    taskResult = None
    message = None
    if streaming:
        response_stream = client.send_message_streaming(
            SendStreamingMessageRequest(
                id=str(uuid4()),
                params=payload,
            )
        )
        async for result in response_stream:
            if isinstance(result.root, JSONRPCErrorResponse):
                print("Error: ", result.root.error)
                return False, contextId, taskId
            event = result.root.result
            contextId = event.contextId
            if (
                isinstance(event, Task)
            ):
                taskId = event.id
            elif (isinstance(event, TaskStatusUpdateEvent)
                  or isinstance(event, TaskArtifactUpdateEvent)
            ):
                taskId = event.taskId
            elif isinstance(event, Message):
                message = event
            print(
                f'stream event => {event.model_dump_json(exclude_none=True)}'
            )
        # Upon completion of the stream. Retrieve the full task if one was made.
        if taskId:
            taskResult = await client.get_task(
                GetTaskRequest(
                    id=str(uuid4()),
                    params=TaskQueryParams(id=taskId),
                )
            )
            taskResult = taskResult.root.result
    else:
        try:
            # For non-streaming, assume the response is a task or message.
            event = await client.send_message(
                SendMessageRequest(
                    id=str(uuid4()),
                    params=payload,
                )
            )
            event = event.root.result
        except Exception as e:
            print("Failed to complete the call", e)
        if not contextId:
            contextId = event.contextId
        if isinstance(event, Task):
            if not taskId:
                taskId = event.id
            taskResult = event
        elif isinstance(event, Message):
            message = event

    if message:
        print(f'\n{message.model_dump_json(exclude_none=True)}')
        return True, contextId, taskId
    if taskResult:
        # Don't print the contents of a file.
        task_content = taskResult.model_dump_json(
            exclude={
                "history": {
                    "__all__": {
                        "parts": {
                            "__all__" : {"file"},
                        },
                    },
                },
            },
            exclude_none=True,
        )
        print(f'\n{task_content}')
        ## if the result is that more input is required, loop again.
        state = TaskState(taskResult.status.state)
        if state.name == TaskState.input_required.name:
            return (
                await completeTask(
                    client,
                    streaming,
                    use_push_notifications,
                    notification_receiver_host,
                    notification_receiver_port,
                    taskId,
                    contextId,
                ),
                contextId,
                taskId,
            )
        ## task is complete
        return True, contextId, taskId
    ## Failure case, shouldn't reach
    return True, contextId, taskId


if __name__ == '__main__':
    asyncio.run(cli())
