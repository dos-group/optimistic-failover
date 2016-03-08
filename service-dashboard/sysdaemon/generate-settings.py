import os
import json

services = []

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
    print('[sysdaemon] Exported settings in settings.json')
    break
  else:
    continue