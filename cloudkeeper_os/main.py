"""
Main entry point for Cloudkeeper-OS
"""
from cloudkeeper_os import configuration
from cloudkeeper_os.grpc import server


def run():
    """
    Main method run for Cloudkeeper-OS
    """
    configuration.configure()
    server.serve()
