# Cloudkeeper-OS
Cloudkeeper-OS is the OpenStack backend for [Cloudkeeper](https://github.com/the-cloudkeeper-project/cloudkeeper). It is using OpenStack Python and gRPC Python libraries.

## Requirements
* Python >= 2.7
* grpcio >= 1.3
* pbr
* python-glanceclient
* python-keystoneauth1
* python-oslo-config
* python-oslo-log

# Installation

To install Cloudkeeper-OS, clone the project and run the ```setup.py``` script:
```
$ git clone https://github.com/the-cloudkeeper-project/cloudkeeper-os.git
$ cd cloudkeeper-os
$ python setup.py install
```

## Configuration

Once the backend is installed, you can generate the configuration file using:
```
mkdir /etc/cloudkeeper-os
oslo-config-generator --config-file etc/cloudkeeper-os/cloudkeeper-os-config-generator.conf --output /etc/cloudkeeper-os/cloudkeeper-os.conf
```

The generated configuration file has several sections and has a descritpion for each option. Most of the options have default values.  You should check at least the following parameters in the ```keystone_authtoken``` section:

* username
* password
* auth_url

In addition, you should have a JSON file containing the map between the VO and the OpenStack project's name:
```
{
    "dteam": {
        "tenant": "EGI_dteam"
    },
    "fedcloud.egi.eu": {
        "tenant": "EGI_FCTF"
    },
    "ops": {
        "tenant": "EGI_ops"
    }
}
```

