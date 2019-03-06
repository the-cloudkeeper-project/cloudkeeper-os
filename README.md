<h1 align="center">
  <img src="https://i.imgur.com/HIqYK2o.png" alt="Logo Cloudkeeper-ONE" title="Logo Cloudkeeper-ONE" width="256"/>
  <p>Cloudkeeper-ONE</p>
</h1>

<h4 align="center">OpenStack backend for <a href="https://github.com/the-cloudkeeper-project/cloudkeeper">Cloudkeeper</a></h4>

## What does Cloudkeeper-OS do?
Cloudkeeper-OS is able to manage [OpenStack](https://www.openstack.org/) CMF - upload, update and remove images and templates representing EGI AppDB appliances. Cloudkeeper-OS runs as a server listening for [gRPC](http://www.grpc.io/) communication usually from core [Cloudkeeper](https://github.com/the-cloudkeeper-project/cloudkeeper) component.

## Requirements
TODO
## Installation
### From PyPi
TODO
### From source (development only)
**Installation from source should never be your first choice! However, if you wish to contribute to our project, this is the right way to start.**
#### Development environment
Cloudkeeper-OS dependencies and packaging are managed via [Poetry](https://poetry.eustace.io/). Poetry has to be installed in order to install dependencies and run tests and linter checks.

To build and install the bleeding edge version from master
```bash
git clone git://github.com/the-cloudkeeper-project/cloudkeeper-os.git
cd cloudkeeper-os
poetry install
poetry run invoke test && poetry run invoke acceptance
```
Cloudkeeper-OS uses [Invoke](http://www.pyinvoke.org/) to run tests and linter checks. There are currently two tasks available:
* `test` - running tests
* `acceptance` - running various linters and security checks

If you want to know what exactly these tasks do, take a look at [tasks.py](tasks.py).
## Configuration
TODO
## Usage
TODO

## Contributing
1. Fork it ( https://github.com/the-cloudkeeper-project/cloudkeeper-os/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request