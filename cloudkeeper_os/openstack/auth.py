"""
Handling of OpenStack authentication methods
"""


from keystoneauth1 import loading
from keystoneauth1 import session

from oslo_config import cfg

from oslo_log import log

import cloudkeeper_os.openstack.exceptions as exceptions

CONF = cfg.CONF
LOG = log.getLogger(__name__)


def auth_session():
    """
    Returns OpenStack authentication session according to configuration

    :return: OpenStack authentication session
    """
    auth_type = CONF.openstack.auth_type
    loader = loading.get_plugin_loader(auth_type)
    auth = loader.load_from_options(**_auth_options(auth_type))
    return session.Session(auth=auth)


def _auth_options(auth_type):
    LOG.debug(f"Requesting auth plugin '{auth_type}'")
    if auth_type == "v3oidcaccesstoken":
        return _v3oidcaccesstoken_options()
    if auth_type == "v3oidcrefreshtoken":
        return _v3oidcrefreshtoken_options()
    if auth_type == "v3applicationcredential":
        return _v3applicationcredential_options()
    if auth_type == "v3password":
        return _v3password_options()

    raise exceptions.UnknownAuthMethod()


def _log_options(func):
    def func_wrapper():
        options = func()
        LOG.debug(f"Auth method options: {options}")
        return options
    return func_wrapper


def _merge_options(func_name):
    def merge_options_decorator(func):
        def func_wrapper():
            return {**func(), **func_name()}
        return func_wrapper
    return merge_options_decorator


def _project_auth_options():
    return {
        "project_name": CONF.openstack.project_name,
        "project_domain_name": CONF.openstack.project_domain_name
    }


def _common_auth_options():
    return {
        "auth_url": f"{CONF.openstack.identity_endpoint}/{CONF.openstack.identity_api_version}",
    }


@_log_options
@_merge_options(_project_auth_options)
@_merge_options(_common_auth_options)
def _v3oidcaccesstoken_options():
    return {
        "access_token": CONF.openstack.oidc_access_token,
        "identity_provider": CONF.openstack.oidc_identity_provider,
        "protocol": CONF.openstack.oidc_protocol,
    }


@_log_options
@_merge_options(_project_auth_options)
@_merge_options(_common_auth_options)
def _v3oidcrefreshtoken_options():
    return {
        "refresh_token": CONF.openstack.oidc_refresh_token,
        "identity_provider": CONF.openstack.oidc_identity_provider,
        "protocol": CONF.openstack.oidc_protocol,
        "client_id": CONF.openstack.oidc_client_id,
        "client_secret": CONF.openstack.oidc_client_secret,
        "discovery_endpoint": CONF.openstack.oidc_discovery_endpoint
    }


@_log_options
@_merge_options(_common_auth_options)
def _v3applicationcredential_options():
    return {
        "application_credential_name": CONF.openstack.application_credential_name,
        "application_credential_secret": CONF.openstack.application_credential_secret,
        "username": CONF.openstack.username,
        "user_domain_name": CONF.openstack.user_domain_name,
    }


@_log_options
@_merge_options(_project_auth_options)
@_merge_options(_common_auth_options)
def _v3password_options():
    return {
        "username": CONF.openstack.username,
        "password": CONF.openstack.password,
        "user_domain_name": CONF.openstack.user_domain_name,
    }
