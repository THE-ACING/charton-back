from grpc import StatusCode
from fastapi import Request
from fastapi.responses import JSONResponse
from grpc.aio import AioRpcError


def grpc_exception_handler(request: Request, exc: AioRpcError) -> JSONResponse:
    match exc.code():
        case StatusCode.NOT_FOUND:
            return JSONResponse(
                status_code=404,
                content={"detail": exc.details()},
            )
        case StatusCode.PERMISSION_DENIED:
            return JSONResponse(
                status_code=403,
                content={"detail": exc.details()},
            )
        case _:
            return JSONResponse(
                status_code=500,
                content={"detail": exc.details()},
            )
