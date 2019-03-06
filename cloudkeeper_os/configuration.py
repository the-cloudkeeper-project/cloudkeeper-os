"""
Configuration and CLI parsing and validation
"""

from os import path

from oslo_config import cfg

from oslo_log import log as logging

import pkg_resources

DEFAULT_GROUP = "DEFAULT"
DEFAULT_OPTIONS = [
    cfg.StrOpt(
        "identifier",
        help="Cloudkeeper-OS instance identifier",
        default="cloudkeeper-os",
        required=True,
    )
]
CONNECTION_OPT_AUTHENTICATION = "authentication"
CONNECTION_OPT_CERTIFICATE = "certificate"
CONNECTION_OPT_KEY = "key"
CONNECTION_OPT_CORE_CERTIFICATE = "core-certificate"
CONNECTION_GROUP = "connection"
CONNECTION_OPTIONS = [
    cfg.StrOpt(
        "listen-address",
        help="IP address Cloudkeeper-OS will listen on",
        default="127.0.0.1:50051",
        required=True,
    ),
    cfg.BoolOpt(
        "authentication",
        help="Client <-> server authentication",
        default=False,
        required=True,
    ),
    cfg.StrOpt(
        "certificate",
        help="Backend's host certificate",
        default="/etc/grid-security/hostcert.pem",
    ),
    cfg.StrOpt(
        "key",
        help="Backend's host key",
        default="/etc/grid-security/hostkey.pem"
    ),
    cfg.StrOpt(
        "core-certificate",
        help="Core's host certificate",
        default="/etc/grid-security/corecert.pem",
    ),
]
APPLIANCES_GROUP = "appliances"
APPLIANCES_OPTIONS = [
    cfg.StrOpt(
        "tmp-dir",
        help="Directory where to temporarily store appliances",
        default="/var/spool/cloudkeeper-os/appliances",
        required=True,
    ),
    cfg.StrOpt(
        "custom-attributes-dir",
        help="Directory with custom attributes specifications",
        sample_default="/etc/cloudkeeper-os/attributes",
    ),
    cfg.StrOpt(
        "visibility",
        help="Visibility of images uploaded to OpenStack",
        choices=["public", "private", "shared", "community"],
        default="private",
        required=True,
    ),
]
OPENSTACK_OPT_AUTH_TYPE = "auth-type"
OPENSTACK_OPT_USERNAME = "username"
OPENSTACK_OPT_PASSWORD = "password"
OPENSTACK_OPT_OIDC_ACCESS_TOKEN = "oidc-access-token"
OPENSTACK_OPT_OIDC_CLIENT_ID = "oidc-client-id"
OPENSTACK_OPT_OIDC_CLIENT_SECRET = "oidc-client-secret"
OPENSTACK_OPT_OIDC_REFRESH_TOKEN = "oidc-refresh-token"
OPENSTACK_OPT_APPLICATION_CREDENTIAL_NAME = "application-credential-name"
OPENSTACK_OPT_APPLICATION_CREDENTIAL_SECRET = "application-credential-secret"
OPENSTACK_AUTH_TYPES = {
    "v3oidcaccesstoken": {
        "description": "Auth via OIDC access token",
        "required": (OPENSTACK_OPT_OIDC_ACCESS_TOKEN,),
    },
    "v3oidcrefreshtoken": {
        "description": "Auth via OIDC refresh token",
        "required": (
            OPENSTACK_OPT_OIDC_CLIENT_ID,
            OPENSTACK_OPT_OIDC_CLIENT_SECRET,
            OPENSTACK_OPT_OIDC_REFRESH_TOKEN,
        ),
    },
    "v3applicationcredential": {
        "description": "Auth via OpenStack's application credentials",
        "required": (
            OPENSTACK_OPT_APPLICATION_CREDENTIAL_NAME,
            OPENSTACK_OPT_APPLICATION_CREDENTIAL_SECRET,
            OPENSTACK_OPT_USERNAME,
        ),
    },
    "v3password": {
        "description": "Auth via username and password",
        "required": (OPENSTACK_OPT_USERNAME, OPENSTACK_OPT_PASSWORD),
    },
}
OPENSTACK_GROUP = "openstack"
OPENSTACK_OPTIONS = [
    cfg.StrOpt(
        "region",
        help="OpenStack region",
        default="default",
        required=True),
    cfg.StrOpt(
        "api-call-timeout",
        help="How long will Cloudkeeper-OS wait for OpenStack to finish operations",
        default="3h",
        required=True,
    ),
    cfg.BoolOpt(
        "allow-remote-source",
        help="Allows OpenStack to directly download remote image",
        default=True,
        required=True,
    ),
    cfg.StrOpt(
        "user-domain",
        help="OpenStack user domain",
        default="default",
        required=True
    ),
    cfg.StrOpt(
        "project-name",
        help="OpenStack project name",
        default="default",
        required=True
    ),
    cfg.StrOpt(
        "project-domain",
        help="OpenStack project domain",
        default="default",
        required=True,
    ),
    cfg.StrOpt(
        "identity-endpoint",
        help="OpenStack Keystone endpoint",
        default="https://identity.localhost:5000",
        required=True,
    ),
    cfg.StrOpt(
        "identity-api-version",
        help="OpenStack Keystone API version",
        default="v3",
        required=True,
    ),
    cfg.StrOpt(
        OPENSTACK_OPT_AUTH_TYPE,
        help="OpenStack authentication method",
        choices=list(
            map(
                lambda key: (key, OPENSTACK_AUTH_TYPES[key]["description"]),
                OPENSTACK_AUTH_TYPES,
            )
        ),
        default="v3oidcaccesstoken",
        required=True,
    ),
    cfg.StrOpt(
        OPENSTACK_OPT_USERNAME,
        help="OpenStack username",
        secret=True
    ),
    cfg.StrOpt(
        OPENSTACK_OPT_PASSWORD,
        help="OpenStack password",
        secret=True
    ),
    cfg.StrOpt(
        OPENSTACK_OPT_OIDC_ACCESS_TOKEN,
        help="OpenStack OIDC access token",
        secret=True
    ),
    cfg.StrOpt(
        OPENSTACK_OPT_OIDC_CLIENT_ID,
        help="OpenStack OIDC client ID",
        secret=True
    ),
    cfg.StrOpt(
        OPENSTACK_OPT_OIDC_CLIENT_SECRET,
        help="OpenStack OIDC client secret",
        secret=True,
    ),
    cfg.StrOpt(
        OPENSTACK_OPT_OIDC_REFRESH_TOKEN,
        help="OpenStack OIDC refresh token",
        secret=True,
    ),
    cfg.StrOpt(
        OPENSTACK_OPT_APPLICATION_CREDENTIAL_NAME,
        help="OpenStack application credential name",
        secret=True,
    ),
    cfg.StrOpt(
        OPENSTACK_OPT_APPLICATION_CREDENTIAL_SECRET,
        help="OpenStack application credential secret",
        secret=True,
    ),
]

PROJECT_NAME = "cloudkeeper-os"
CONF_DIRS = (
    path.join(path.dirname(__file__), "..", "config"),
    path.join(path.sep, "etc", "cloudkeeper-os"),
    path.join(path.expanduser("~"), ".cloudkeeper-os"),
)


def configure():
    """
    Parse configuration and CLI options and validates their sanity
    :return: configuration dictionary with configuration options
    """
    conf = cfg.CONF

    # [DEFAULT]
    _configure_options(conf, DEFAULT_OPTIONS)
    # [connection]
    _configure_options(conf, CONNECTION_OPTIONS, CONNECTION_GROUP)
    # [appliances]
    _configure_options(conf, APPLIANCES_OPTIONS, APPLIANCES_GROUP)
    # [openstack]
    _configure_options(conf, OPENSTACK_OPTIONS, OPENSTACK_GROUP)

    logging.register_options(conf)
    logging.setup(conf, PROJECT_NAME)

    conf(default_config_dirs=CONF_DIRS,
         project=PROJECT_NAME,
         version=pkg_resources.get_distribution(PROJECT_NAME).version
         )

    _validate_configuration(conf)

    return conf


def _configure_options(conf, options, group=None):
    conf.register_opts(options, group=group)
    conf.register_cli_opts(options, group=group)


def _validate_configuration(conf):
    _validate_configuration_group(
        conf,
        CONNECTION_OPT_AUTHENTICATION,
        True,
        (
            CONNECTION_OPT_CERTIFICATE,
            CONNECTION_OPT_KEY,
            CONNECTION_OPT_CORE_CERTIFICATE,
        ),
        CONNECTION_GROUP,
    )
    _validate_auth_groups(conf)


def _validate_auth_groups(conf):
    for auth_type, data in OPENSTACK_AUTH_TYPES.items():
        _validate_configuration_group(
            conf,
            OPENSTACK_OPT_AUTH_TYPE,
            auth_type,
            data["required"],
            OPENSTACK_GROUP,
        )


def _validate_configuration_group(conf, main_option, value, options, group):
    if conf[group][main_option.replace("-", "_")] != value:
        return

    for opt in options:
        if not conf[group][opt.replace("-", "_")]:
            raise cfg.RequiredOptError(opt, cfg.OptGroup(group))


def list_opts():
    """
    Entry point for oslo.config so default configuration can be generated automatically
    :return: configuration groups and their options
    """
    return (
        (DEFAULT_GROUP, DEFAULT_OPTIONS),
        (CONNECTION_GROUP, CONNECTION_OPTIONS),
        (APPLIANCES_GROUP, APPLIANCES_OPTIONS),
        (OPENSTACK_GROUP, OPENSTACK_OPTIONS),
    )
