try:
    import logging
    import time
    from typing import Dict, List, Union

    from starlette.middleware.base import (
        BaseHTTPMiddleware,
        DispatchFunction,
        RequestResponseEndpoint,
    )
    from starlette.requests import Request
    from starlette.responses import JSONResponse, Response
    from starlette.types import ASGIApp

    logger = logging.getLogger(__name__)

    DEFAULT_UNEXPECTED_RESPONSE = JSONResponse(
        {"message": "Internal Server Error"}, status_code=500
    )

    class LogNinjaMiddleware(BaseHTTPMiddleware):
        def __init__(
            self,
            app: ASGIApp,
            dispatch: DispatchFunction | None = None,
            unexpected_exception_response: JSONResponse = DEFAULT_UNEXPECTED_RESPONSE,
            unexpected_exception_log: str = "An unexpected exception occurred",
            contextvars: List = [],
        ) -> None:
            self.unexpected_exception_log = unexpected_exception_log
            self.contextvars = contextvars
            self.unexpected_exception_response = unexpected_exception_response
            super().__init__(app, dispatch=dispatch)

        async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
        ) -> Response:
            start_time = time.perf_counter_ns()
            try:
                response = await call_next(request)
            except Exception as e:
                logger.info(self.unexpected_exception_log, stack_info=e)
                raise
            finally:
                process_time = time.perf_counter_ns() - start_time

                status_code = response.status_code
                url = self._get_path_with_query_string(request.scope)
                client_host = request.client.host
                client_port = request.client.port
                http_method = request.method
                http_version = request.scope["http_version"]

                logger.info(
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

                response.headers["X-Process-Time"] = str(process_time / 10**9)
                return response

        def _get_path_with_query_string(self, scope: Dict[str, Union[str, bytes]]):
            query_string = scope.get("query_string", b"").decode()
            path = scope.get("path", "")
            full_path = f"{path}?{query_string}" if query_string else path
            return full_path

except ImportError:
    raise ImportError(
        "LogNinjaMiddleware requires starlette to be installed, install it with `pip install logninja[starlette]`."
    )
