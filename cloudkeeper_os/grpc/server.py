"""
gRPC server wrapper
"""
import time
from concurrent import futures

import grpc

from oslo_config import cfg

from cloudkeeper_os.grpc import cloudkeeper_pb2_grpc
from cloudkeeper_os.grpc.core_connector import CoreConnector


CONF = cfg.CONF
ONE_DAY_IN_SECONDS = 60 * 60 * 24
GRACE_PERIOD = 5


def serve():
    """
    Configure and start gRPC server
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cloudkeeper_pb2_grpc.add_CommunicatorServicer_to_server(
        CoreConnector(),
        server
    )
    server.add_secure_port(CONF.connection.listen_address, _credentials())
    server.start()
    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except (KeyboardInterrupt, SystemExit):
        server.stop(GRACE_PERIOD)


def _credentials():
    if not CONF.connection.authentication:
        return grpc.ServerCredentials(None)

    with open(CONF.connection.key, 'rb') as key_file:
        key = key_file.read()

    with open(CONF.connection.certificate, 'rb') as cert_file:
        certificate = cert_file.read()

    with open(CONF.connection.core_certificate, 'rb') as core_cert_file:
        core_certificate = core_cert_file.read()

    return grpc.ssl_server_credentials((key, certificate), core_certificate, True)
