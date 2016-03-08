#!/bin/sh

cd /opt
apt-get --assume-yes --force-yes install git python3-psutil python3-requests -f
git clone https://github.com/citlab/optimistic-failover.git
cp service-dashboard/sysdaemon/sysdaemon.conf /etc/init/
initctl reload-configuration
initctl start sysdaemon