# Service Dashboard

Dashboard for a view over the running OpenStack instances and the running services. 
![alt text](https://raw.githubusercontent.com/citlab/optimistic-failover/master/screenshots/dashboard.png "dashboard preview")

## Requirements for the Dashboard

For a successful installation you need:
* a working python3.4 environment with pip installed
* python virtualenv installed
* The OpenStack user data

## Installation Notes for the Dashboard

1. Clone this repository
  * `git clone <repository url>`
  * `cd service-dashboard`

2. Install a virtual python environment and install novaclient
  * `virtualenv --python=python3 env`
  * `source env/bin/activate`
  * `pip install python-novaclient`
 
3. Configuration
  * open `servicedashboard/views.py`
  * edit the OpenStack credentials at the beginning of the file

3. Install and run
  * `python3 setup.py develop` (this may take some time)
  * `pserve development.ini`
  * `surf http://<adress of your server>:6543`

4. (optional) create a configuration file for initctl to autostart the example service and to track the condition with the service dashboard.

To see the running services and the CPU and RAM utilization, the sysdaemon needs to be installed on the OpenStack instances.

## Requirements of the sysdaemon
* a working python 2.7 environment with pip installed
* only tested with ubuntu 14.04, essentially a working initctl is needed to track the status of the services

## Installation for the sysdaemon

1. Install the requirements
  * `pip install psutil`
  * `pip install requests`
  * Copy the sysdaemon.py to a desired directory, for example `/opt/sysdaemon`

2. Configuration
  * Edit the IP/Port of the dashboard in the very beginning of the file `sysdaemon.py`
  * The sysdaemon creates a `settings.json` file if no such file exist. Set the system variable `sdsettings` to the desired path of the settigns file by `export sdsettings=/path/to/settings.json`

3. Run the sysdaemon
  * `python sysdaemon.py` 
  * Install the missing dependencies if there are any
  * Follow the dialog and state the services that are running. The name of the services needs to match with the service name based on ubuntus initctl exactly.

From now on, the sysdaemon should periodically track the health of the services and send the CPU and RAM utilization to the dashboard. The dashboard should indicate the health by the color of the service.
