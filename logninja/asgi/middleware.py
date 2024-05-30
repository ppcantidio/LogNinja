import contextvars
import logging
import time
from dataclasses import dataclass, field
from typing import List, Tuple

from starlette import status
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from logninja.logger import logger as logninja_logger


@dataclass
class LogNinjaASGIMiddleware:
    app: ASGIApp

    logger: logging.Logger = logninja_logger
    contextvars_by_headers: List[
        contextvars.ContextVar | Tuple[contextvars.ContextVar, str]
    ] = field(default_factory=lambda: [])
    contextvars_by_app_state: List[contextvars.ContextVar] = field(
        default_factory=lambda: []
    )

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        headers = MutableHeaders(scope=scope)
        await self._set_contextvars_by_headers(headers)
        await self._set_contextvars_by_app_state(scope)

        request = Request(scope, receive, send)

        async def send_with_extra_headers(message: Message):
            if message["type"] == "http.response.start":
                process_time = time.perf_counter_ns() - start_time
                status_code = message.get("status")
                await self._log_finish(request, status_code, process_time)
            await send(message)

        start_time = time.time()
        try:
            await self.app(scope, receive, send_with_extra_headers)
        except Exception as exc:
            process_time = time.perf_counter_ns() - start_time
            self.logger.exception(
                "An error occurred while processing the request",
                stack_info=True,
                exc_info=exc,
            )
            await self._log_finish(
                request, status.HTTP_500_INTERNAL_SERVER_ERROR, process_time
            )
            response = JSONResponse(
                content={"message": "Internal Server Error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            await response(scope, receive, send)

    async def _log_finish(
        self, request: Request, status_code: int, process_time: float
    ):
        url = await self._get_path_with_query_string(request.scope)
        client_host = request.client.host
        client_port = request.client.port
        http_method = request.method
        http_version = request.scope["http_version"]

        self.logger.info(
            f"""{client_host}:{client_port} - "{http_method} {url} HTTP/{http_version}" {status_code}""",
            extra={
                "http": {
                    "url": url,
                    "method": http_method,
                    "status_code": status_code,
                    "version": http_version,
                },
                "network": {"client": {"ip": client_host, "port": client_port}},
                "duration": process_time,
            },
        )

    async def _set_contextvars_by_headers(self, headers: MutableHeaders) -> None:
        for contextvar in self.contextvars_by_headers:
            header_name = (
                contextvar.name
                if isinstance(contextvar, contextvars.ContextVar)
                else contextvar[1]
            )
            if headers.get(header_name) is not None:
                contextvar.set(headers.get(header_name))

    async def _set_contextvars_by_app_state(self, scope: Scope) -> None:
        for contextvar in self.contextvars_by_app_state:
            if hasattr(scope.get("app").state, contextvar.name) is not None:
                contextvar.set(scope.get(contextvar.name))

    async def _get_path_with_query_string(self, scope: Scope):
        query_string = scope.get("query_string", b"").decode()
        path = scope.get("path", "")
        full_path = f"{path}?{query_string}" if query_string else path
        return full_path
