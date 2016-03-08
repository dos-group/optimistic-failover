import psutil
import time
import requests
import os.path
import os
import json
import threading
import subprocess
import sys
import socket

'''
This little script reports the cpu_percent and 
virtual_memory to the service dashboard.

psutil must be installed
'''
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 9000 # Arbitrary non-privileged port

DASHBOARD = "http://10.0.0.26:6542" # IP of the service-dashboard

services = list()

def main():
  global services

  print('[sysdaemon] started sysdaemon')
  dir = os.path.dirname(__file__)
  services = json.load(open(os.path.join(dir,'settings.json'), 'r'))

  for service in services:
    call_dashboard(service)
    sthread = threading.Thread(target=service_thread, args=(service,))
    sthread.start()

  while True:
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=1)

    try:
      data = requests.post(DASHBOARD+'/api/sys',data=
        {'ram': str(ram),
         'cpu': str(cpu)
        })
      data.connection.close()
    except:
      print('[sysdaemon] error while connection to dashboard, trying again')
      time.sleep(5)
    time.sleep(1)

############ internal methods ##############

def call_dashboard(service):
  print('[sysdaemon] service is calling dashboard')
  try:
    data = requests.post(DASHBOARD+'/api/call',data=
    {'host': str(socket.gethostname()),
     'type': service['dbname'],
     'running': service['running']
    })
    instruction = data.json()['instruction']
    return str(instruction)
    data.connection.close()
  except:
    print('[sysdaemon] error, could not call dashboard, trying again')
    time.sleep(5)
    call_dashboard(service)

def service_thread(service):
  while True:
    initctl_status = subprocess.check_output(['initctl','status',service['init']], universal_newlines=True)
    if initctl_status.split(' ')[1] == 'start/running,':
      service['running'] = True
    else:
      service['running'] = False
    instruction = call_dashboard(service)
    if instruction == 'start':
      subprocess.check_output(['initctl','start',service['init']], universal_newlines=True)
      continue
    elif instruction == 'stop':
      subprocess.check_output(['initctl','stop',service['init']], universal_newlines=True)
      continue

    time.sleep(3)

#############################################

if __name__ == "__main__":
    main()
