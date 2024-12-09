import grpc

from app.settings import settings
from services.track import track_pb2_grpc

channel = grpc.insecure_channel(f'{settings.TRACK_SERVICE_GRPC_HOST}:{settings.TRACK_SERVICE_GRPC_PORT}')
track_service = track_pb2_grpc.TrackStub(channel)