# Service Dashboard

Dashboard for a view over the running OpenStack instances and the running services. 

## Requirements

For a successful installation you need:
* a working python3.4 environment with pip installed
* python virtualenv installed

## Installation Notes

1. Clone this repository
  * `git clone <repository url>`
  * `cd service-dashboard`

2. Install a virtual python environment
  * `virtualenv --python=python3 env`
  * `source env/bin/activate`

3. Install and run
  * `python3 setup.py develop` (this may take some time)
  * `pserve development.ini`
  * `surf http://<adress of your server>:6542`
  
If the installation is unsuccessful try installing `pip install python-novaclient`
  
## Documentation
Please read the full documentation in the wiki.