# optimistic-failover

Python implementation of a service-dashboard and example services for experiments with an optimistic failover. The dashboard and the note-taking example service is developed with the [pyramid framework](http://www.pylonsproject.org/) for site generation and [bootstrap](http://getbootstrap.com/) for fancy mobile-first layouts. The dashboard requires an OpenStack installation since the displayed servers are extracted from the installation via novaclient. The example service are stateful services with implemented optimistic replication mechanisms.

service-dashboard:
![alt text](https://raw.githubusercontent.com/citlab/optimistic-failover/master/screenshots/dashboard.png "dashboard preview")

note-taking example service:
![alt text](https://raw.githubusercontent.com/citlab/optimistic-failover/master/screenshots/notetaking.png "notetaking preview")

## Requirements

For a successful installation you need:
* an OpenStack installation with the corresponding credentials and permissions to start/stop/pause servers
* a working Linux environment with a proper python installation (we only tested our tools on linux machines)

The documentation of the dashboard and the example services can be found in the corresponding README files:
* [service-dashboard README](https://github.com/citlab/optimistic-failover/tree/master/service-dashboard)
* [note-taking example service README](https://github.com/citlab/optimistic-failover/tree/master/example-services/note-taking)

## Publications

More documentation and publications will be added later.
