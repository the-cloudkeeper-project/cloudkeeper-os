# Cloudkeeper-OS
Cloudkeeper-OS is the OpenStack backend for [Cloudkeeper](https://github.com/the-cloudkeeper-project/cloudkeeper)

## Requirements
* Python >= 2.7

## Installation

To install Cloudkeeper-OS, clone the project and run the setup.py script. The following line do the work: 
```
python setup.py install
```

## Configuration

Once the backend is installed, you can generate the configuration file using:
```
oslo-config-generator --config-file etc/cloudkeeper-os/cloudkeeper-os-config-generator.conf
```

