"""
Main entry point for Cloudkeeper-OS
"""
from cloudkeeper_os import configuration
from cloudkeeper_os.grpc import server

# poetry run cloudkeeper-os --openstack-identity-endpoint=http://147.251.253.3/identity --openstack-auth-type=v3password --openstack-username=demo --openstack-password=openstack --openstack-user-domain-name=default --openstack-project-name=demo --openstack-region-name=RegionOne  --openstack-project-name=demo -d
def run():
    """
    Main method run for Cloudkeeper-OS
    """
    configuration.configure()
    server.serve()
