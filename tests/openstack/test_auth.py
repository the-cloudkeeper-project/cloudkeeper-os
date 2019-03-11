"""
Testing OpenStack authentication methods
"""


import keystoneauth1

from oslo_config import fixture

import pytest

import cloudkeeper_os.openstack.auth as auth
import cloudkeeper_os.configuration as configuration


@pytest.fixture
def _config():
    """
    Fixture preparing dummy configuration for tests
    """
    cfg = fixture.Config()
    cfg.setUp()
    cfg.register_opts(configuration.OPENSTACK_OPTIONS, configuration.OPENSTACK_GROUP)
    return cfg


@pytest.mark.parametrize(
    "config_options,expected",
    [
        (
            {
                "group": "openstack",
                "auth_type": "v3oidcaccesstoken",
                "oidc_access_token": "token",
                "oidc_identity_provider": "IP",
                "oidc_protocol": "protocol"
            },
            "v3oidcaccesstoken"
        ),
        (
            {
                "group": "openstack",
                "auth_type": "v3oidcrefreshtoken",
                "oidc_refresh_token": "token",
                "oidc_identity_provider": "IP",
                "oidc_protocol": "protocol",
                "oidc_client_id": "ID",
                "oidc_client_secret": "secret",
                "oidc_discovery_endpoint": "endpoint"
            },
            "v3oidcrefreshtoken"
        ),
        (
            {
                "group": "openstack",
                "auth_type": "v3applicationcredential",
                "application_credential_name": "name",
                "application_credential_secret": "secret",
            },
            "v3applicationcredential"
        ),
        (
            {
                "group": "openstack",
                "auth_type": "v3password",
                "username": "name",
                "password": "secret",
            },
            "v3password"
        )
    ])
def test_auth_session(mocker, _config, config_options, expected):
    """
    Testing creation of multiple authentication method handlers based on the passed configuration options
    """
    _config.config(**config_options)
    spy = mocker.spy(keystoneauth1.loading, "get_plugin_loader")
    assert auth.auth_session()
    spy.assert_called_once_with(expected)
