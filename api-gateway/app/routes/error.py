import grpc
from fastapi import Request
from fastapi.responses import JSONResponse


async def grpc_exception_handler(request: Request, exc: grpc.RpcError):
    status_code = 500
    detail = "Internal Server Error"

    return JSONResponse(
        status_code=status_code,
        content={"detail": detail},
    )