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

  # TODO: check if path exists and catch exception

  if os.path.exists(str(os.environ['sdsettings'])):
    with open(str(os.environ['sdsettings']), 'r') as outfile:
      services = json.load(outfile)
  else:
    generate_settings()

  for service in services:
    call_dashboard(service)
    sthread = threading.Thread(target=service_thread, args=(service,))
    sthread.start()

  print('[sysdaemon] starting sys thread')
  sys = threading.Thread(target=sys_thread)
  sys.start()


  while True:
    time.sleep(10)

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

def sys_thread():
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

def generate_settings():
  global services

  print('[sysdaemon] Settings dialog, please answer the following questions:')
  while True:
    print('[sysdaemon] Do you want to add a service?')
    answer = input('> ')
    if str(answer) == 'yes':
      print('[sysdaemon] Name of the service based on initctl?')
      init = input('> ')
      print('[sysdaemon] Name of the service to appear in dashboard?')
      dbname = input('> ')
      print('[sysdaemon] ############################')
      print('[sysdaemon] initctl name: ',init)
      print('[sysdaemon] dashboard name: ',dbname)
      print('[sysdaemon] ############################')
      print('[sysdaemon] Is this information correct?')
      answer = input('> ')
      if str(answer) == 'yes':
        services.append({'init': init, 'dbname': dbname, 'running': False})
        with open('settings.json', 'w') as outfile:
          json.dump(services, outfile)
    elif str(answer) == 'no':
      print('[sysdaemon] Exported settings in:',os.path.abspath('settings.json'))
      print('[sysdaemon] Please set this path as the sdsettings environment variable.')
      break
    else:
      continue

#############################################

if __name__ == "__main__":
    main()
