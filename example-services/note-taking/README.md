# CRDT Note Taking Example Service

Note Taking Example Service implemented with Conflict-free Replicated Data Types.

![alt text](https://raw.githubusercontent.com/citlab/optimistic-failover/master/screenshots/notetaking.png "notetaking preview")

## Requirements for the Note Taking App

For a successful installation you need:
* a working python3.4 environment with pip installed
* python virtualenv installed
* (optional) MySQL and the python3 MySQL-connector installed

## Installation Notes for the Dashboard

1. Clone this repository
  * `git clone <repository url>`
  * `cd example-services/note-taking`

2. Install a virtual python environment
  * `virtualenv --python=python3 env`
  * `source env/bin/activate`
 
3. Configuration
  * The current configuration works with a local sqlite database. If a MySQL database is desired, the corresponding lines in the `development.ini` needs to be edited and the user data and ip of the database needs to be added. This step is not needed if sqlite is the desired database.

3. Install and run
  * `python3 setup.py develop` (this may take some time)
  * `pserve development.ini`
  * `surf http://<adress of your server>:6543`

## Requirements of the traffic-generator

* essentially the same requirements as the note-taking application

## Installation/run of the traffic-generator

1. Configuration
  * Edit the IP/Port of the app in the very beginning of the file `traffic-generator/trafficgenerator.py`

2. Run the traffic-generator
  * `cd traffic-generator`
  * `python trafficgenerator.py` 
  * Install the missing dependencies if there are any
