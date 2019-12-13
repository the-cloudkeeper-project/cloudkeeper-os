"""
OpenStack Glance client access
"""


from glanceclient import Client

from oslo_config import cfg

from oslo_log import log

from cloudkeeper_os.openstack import auth

CONF = cfg.CONF
LOG = log.getLogger(__name__)
GLANCE_CLIENT_VERSION = "2"


def client():
    """
    Returns a Glance client instance based on configuration
    :return: Glance client instance
    """
    LOG.debug(
        f"Retrieving Glance client for region '{CONF.openstack.region_name}' \
                and interface '{CONF.openstack.glance_interface}'"
    )
    session = auth.auth_session()
    endpoint = session.get_endpoint(
        service_type="image",
        interface=CONF.openstack.glance_interface,
        region_name=CONF.openstack.region_name,
    )
    return Client(GLANCE_CLIENT_VERSION, endpoint, session=session)
