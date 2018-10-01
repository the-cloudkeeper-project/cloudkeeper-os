==============
Cloudkeeper-OS
==============

Cloudkeeper-OS is a project that provides an `OpenStack Glance <https://docs.openstack.org/glance>`_
backend for `Cloudkeeper <https://github.com/the-cloudkeeper-project/cloudkeeper>`_.
It interacts with the OpenStack Image Service to manage images representing
`EGI AppDB <https://appdb.egi.eu/browse/cloud>`_ Appliances. Cloudkeeper-OS
runs as a server listening for `gRPC <https://grpc.io/>`_ communication from
Cloudkeeper.

Use the following resources to learn more:

Developers
----------

For information on how to contribute to Glance, please see the contents
of the ``CONTRIBUTING.rst`` file in this repository.

Any new code must follow the development guidelines detailed in the
``HACKING.rst`` file, and pass all unit tests.


Installation
------------

From source
===========

The **cloudkeeper-os** program has several dependencies listed in the
``requirements.txt`` file.

*Cloudkeeper-OS* can be downloaded from the following
`GitHub repository <https://github.com/the-cloudkeeper-project/cloudkeeper-os>`_::

  $ git clone https://github.com/the-cloudkeeper-project/cloudkeeper-os.git

In the created directory, run the ``setup.py`` script::

  $ git clone https://github.com/the-cloudkeeper-project/cloudkeeper-os.git
  $ cd cloudkeeper-os
  $ python setup.py install
  $ mkdir /etc/cloudkeeper-os
  $ cp etc/cloudkeeper-os.conf.sample /etc/cloudkeeper-os/cloudkeeper-os.conf
  $ cp etc/cloudkeeper-os/mapping.json /etc/cloudkeeper-os/mapping.json

Create the ``/usr/lib/systemd/system/cloudkeeper-os.service`` systemd service
file with the following content to manage the **cloudkeeper-os** daemon::

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


Using RPMs
==========

First, download the *repo* file from the `cloudkeeper-os repository <ihttp://repository.egi.eu/community/software/cloudkeeper.os/0.9.x/releases/repofiles/centos-7-x86_64.repo>`_
place it in the ``/etc/yum.repos.d`` directory. Then execute the following
commands::

  $ yum update
  $ yum install cloudkeeper-os


Configuration
-------------

The ``cloudkeeper-os.conf`` configuration file has several sections and has a
descritpion for each option. Most of the options have default values.  You
should check at least the following parameters in the *keystone_authtoken*
section:

* username
* password
* auth_url

For example::

  [keystone_authtoken]
  username = cloudkeeper
  password = cloudkeeper
  auth_url = http://controller:5000/v3


In addition, you have to edit the ``mapping.json`` JSON file to map correctly the
VO and the OpenStack project's name. Note that you can use the same JSON file
as for the `keystone-voms <https://ifca.github.io/keystone-voms/>`_ component,
by setting the *mapping_file* parameter with the path to ``mapping.json`` file
in the ``cloudkeeper-os.conf`` file (this file is called ``voms.json`` in the
keystone-voms project).

Note that the user defined by the *username* parameter should have the right
to manage the images for all the project defined in the ``mapping.json`` file.

To take into account the modifications, do not forget to restart the
*cloudkeeper-os* service.
