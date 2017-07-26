# Cloudkeeper-OS
Cloudkeeper-OS is an OpenStack backend for [Cloudkeeper](https://github.com/the-cloudkeeper-project/cloudkeeper). It interacts with the OpenStack Image Service ([Glance](https://docs.openstack.org/glance)) to manage images representing [EGI AppDB](https://appdb.egi.eu/browse/cloud) Appliances. Cloudkeeper-OS runs as a server listening for [gRPC](https://grpc.io/) communication, usually from Cloudkeeper.

## Requirements
* Python >= 2.7
* grpcio >= 1.3
* pbr
* python-glanceclient
* python-keystoneauth1
* python-oslo-config
* python-oslo-log

## Installation

### From source
To install Cloudkeeper-OS, clone the project and run the ```setup.py``` script:
```
$ git clone https://github.com/the-cloudkeeper-project/cloudkeeper-os.git
$ cd cloudkeeper-os
$ python setup.py install
$ mkdir /etc/cloudkeeper-os
$ cp etc/cloudkeeper-os.conf.sample /etc/cloudkeeper-os/cloudkeeper-os.conf
$ cp etc/cloudkeeper-os/voms.json /etc/cloudkeeper-os/voms.json
```

Create the ```/usr/lib/systemd/system/cloudkeeper-os.service``` systemd service file with the following content to manage the cloudkeeper-os daemon:
```
[Unit]
Description=OpenStack Cloudkeeper Backend
After=syslog.target network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/cloudkeeper-os
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Using RPMs

First, download the repo file from the [cloudkeeper-os repository](http://grand-est.fr/resources/software/cloudkeeper-os/repofiles/centos7/cloudkeeper-os.repo) and place it in the ```/etc/yum.repos.d``` directory. Then execute the following commands:
```
$ yum update
$ yum install cloudkeeper-os
```

## Configuration

The ```cloudkeeper-os.conf``` configuration file has several sections and has a descritpion for each option. Most of the options have default values.  You should check at least the following parameters in the ```keystone_authtoken``` section:

* username
* password
* auth_url

In addition, you have to edit the ```voms.json``` JSON file to map correctly the VO and the OpenStack project's name. Note that you can use the same JSON file as for the ```keystone-voms``` component, by setting the ```mapping_file``` parameter with the right path in the ```cloudkeeper-os.conf``` file.

Note that the user defined by the ```username``` parameter in the ```cloudkeeper-os.conf``` file should have the right to manage the images for all the project defined in the ```voms.json``` file.

To take into account the modifications, do not forget to restart the cloudkeeper-os service.
