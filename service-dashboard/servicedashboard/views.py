from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPOk
from novaclient import client

import threading
import time
import copy
import requests
import datetime

services = [] # the list of all services

vservers = [] # the list of serverswhich are extracted out of openstack/nova

# OpenStack interface:
nova = client.Client(2,'username','password','project','http://OpenStack-controller')
nova_net = 'network name'

############## views ##############

@view_config(route_name='home', renderer='home.mako')
def home_view(request):
  """Manages the view for the / site

  Args:
    request: typically an empty http GET request

  Returns:
    A dict with basic project information such as services and servers
  """
  return {'project': 'service-dashboard',
          'services': services,
          'vservers': vservers
         }

'''
@view_config(route_name='save')
def save_view(request):
  """Manages the save button of the traffic generation

  If a checkbox is selected, this method starts a thread for the corresponding
  service. The thread generates traffic to that service via the generate_traffic
  method.

  Args:
    request: typically a http POST request with the id's of the selected 
    checkboxes. For example: id1

  Returns:
    A redirect to the refreshed home site.
  """
  global services

  for index, service in enumerate(services):

    if 'id' + str(index) in request.params:
      traffic_temp = service['traffic']
      service['traffic'] = True

      if traffic_temp == False:
        gen_thread = threading.Thread(target=generate_traffic, args=(index,))
        gen_thread.start()
    else:
      service['traffic'] = False

  return HTTPFound(location='/')

@view_config(route_name='dsave')
def dsave_view(request):
  global services

  for index, service in enumerate(services):

    if 'id' + str(index) in request.params:
      traffic_temp = service['dtraffic']
      service['dtraffic'] = True

      if traffic_temp == False:
        gen_thread = threading.Thread(target=generate_delete_traffic, args=(index,))
        gen_thread.start()
    else:
      service['dtraffic'] = False

  return HTTPFound(location='/')
'''

@view_config(route_name='delservice')
def delservice_view(request):
  global services
  index = request.matchdict['id']
  index = int(index)

  services.pop(index)
  return HTTPFound(location='/')

@view_config(route_name='servers', renderer='json')
def servers_view(request):
  """Manages ajax request for the cpu and ram utilization

  Args:
    request: typically an empty http GET request

  Returns:
    A dict with information about the servers
  """
  return {'vservers' : vservers}

@view_config(route_name='services', renderer='json')
def services_view(request):
  global services
  """Manages ajax request for the services

  Args:
    request: typically an empty http GET request

  Returns:
    A dict with information about the services
  """


  #current_time = datetime.datetime.now()

  #for service in services:
  #  if (current_time - service['heartbeat']).total_seconds() > 3:
  #    service['running'] = 'False'

  return {'services' : services}
  

@view_config(route_name='vservers')
def vservers_view(request):
  """Manages the button click for a refresh of the servers out of openstack

  The method initiates an update of the server informations via the method
  get_vservers()

  Args:
    request: typically an empty http GET request

  Returns:
    A redirect to the updated home page.
  """
  get_vservers()
  return HTTPFound(location='/')

@view_config(route_name='start_instructions')
def start_instructions_view(request):
  global services
  index = int(request.matchdict['id'])
  services[index]['instruction'] = 'start'
  return HTTPFound(location='/')

@view_config(route_name='stop_instructions')
def stop_instructions_view(request):
  global services
  index = int(request.matchdict['id'])
  services[index]['instruction'] = 'stop'
  return HTTPFound(location='/')

@view_config(route_name='vservers_stop')
def vservers_stop_view(request):
  s_id = str(request.matchdict['id'])
  for index,server in enumerate(vservers):
    if server['id'] == s_id:
      nova.servers.list()[index].stop()
      break
  return HTTPFound(location='/vservers')

@view_config(route_name='vservers_start')
def vservers_start_view(request):
  s_id = str(request.matchdict['id'])
  for index,server in enumerate(vservers):
    if server['id'] == s_id:
      nova.servers.list()[index].start()
      break
  return HTTPFound(location='/vservers')

@view_config(route_name='vservers_reboot')
def vservers_reboot_view(request):
  s_id = str(request.matchdict['id'])
  for index,server in enumerate(vservers):
    if server['id'] == s_id:
      nova.servers.list()[index].reboot()
      break
  return HTTPFound(location='/vservers')

@view_config(route_name='vservers_pause')
def vservers_pause_view(request):
  s_id = str(request.matchdict['id'])
  for index,server in enumerate(vservers):
    if server['id'] == s_id:
      nova.servers.list()[index].pause()
      break
  return HTTPFound(location='/vservers')

@view_config(route_name='vservers_unpause')
def vservers_unpause_view(request):
  s_id = str(request.matchdict['id'])
  for index,server in enumerate(vservers):
    if server['id'] == s_id:
      nova.servers.list()[index].unpause()
      break
  return HTTPFound(location='/vservers')

############## api views ##############

@view_config(route_name='api_sys', renderer='json')
def api_sys_view(request):
  """Manages an api update of the ram and cpu information of the clients

  Args:
    request: typically a http POST request with a 'ram' and a 'cpu' parameter
    representing the current ram usage and cpu utilization

  Returns:
    A redirect to the updated home page.
  """
  global vservers, services
  ip = str(request.client_addr)
  ram = request.params['ram']
  cpu = request.params['cpu']

  for server in vservers:
    if ip in server['ip']:
      server['ram'] = ram
      server['cpu'] = cpu

  return {'status':'ok'}

@view_config(route_name='api_call', renderer='json')
def api_call_view(request):
  """Manages an api update of the services

  Each time a new service joins the network the api_call method is called. The
  method informs all other connected services about the new service and updates
  the global variables. If the service was already in the dashboard, the other
  services will not notified.

  Args:
    request: typically a http POST request with a 'host' and a 'port' and a 
    'type'parameter. Hereby the 'type' parameter is simple the information what
    kind of service is calling.
    
  Returns:
    A dict of the existing services before the call. The return value is 
    important for the calling service gets the information about the already
    connected services.
  """
  global services
  ip = str(request.client_addr)
  host = request.params['host']
  #port = str(request.params['port'])
  apptype = request.params['type']
  running = request.params['running']

  '''
  nservices = copy.deepcopy(services)

  for index, service in enumerate(nservices):
    if service['ip'] == ip and service['port'] == port:
      nservices.pop(index)
      return {'services': nservices}

  notify_services(nservices,ip,port)
  '''
  
  for index,service in enumerate(services):
    if service['host'] == host and service['type'] == apptype:
      service['running'] = running
      #service['heartbeat'] = datetime.datetime.now()
      return_instruction = service['instruction']
      service['instruction'] = ''
      return {'instruction':return_instruction}

  services.append(
    { 'type': apptype,
      'ip': ip,
      'host': host,
      'running': running,
      #'heartbeat': datetime.datetime.now(),
      'instruction': ''
    }
  )
  return {'instruction':''}
  
############ internal methods ##############
'''
def notify_services(nservices, ip, port):
  # all services in nservices are informed about a new service at ip:port
  for service in nservices:
    requests.post('http://' + service['ip'] +
                  ':' + service['port'] + '/api/addpeer', 
                  data={'ip':ip,'port':port})

'''

'''

def generate_traffic(index):
  # this method is executed by a thread when a checkbox is selected.
  while services[index]['traffic']:
    r = requests.post('http://' + services[index]['ip'] + ':' 
                      + services[index]['port'] + '/api/compose',
                      data={'msg':'generated message'})
    time.sleep(0.001)

def generate_delete_traffic(index):
  # this method is executed by a thread when a checkbox is selected.
  while services[index]['dtraffic']:
    r = requests.post('http://' + services[index]['ip'] + ':' 
                      + services[index]['port'] + '/api/invoke_delete',
                      data={'msgid':'RANDOM'})
    time.sleep(0.01)
'''

def get_vservers():
  # extract the information of all existing servers out of the nova client
  # the auth server should be resolved as controller.
  global vservers
  nvservers = []

  for index,server in enumerate(nova.servers.list()):
    image_id = server.image['id']
    image_name = ''

    for image in nova.images.list():
      if image.id == image_id:
        image_name = image.name

    nvservers.append({
      'id' : server.id,
      'name': server.name,
      'status_info': server.status,
      'ip': ', '.join(server.networks[nova_net]) if nova_net in server.networks else '',
      'os': image_name,
      'host': 'unknown',
      'ram': 0,
      'cpu' : 0
      })

  vservers = nvservers

def vserver_thread():
  global vservers

  while True:
    try:
      time.sleep(4)
      for vserver in vservers:
        vserver['reported'] = False 
      for server in nova.servers.list():
        found_server = False
        for index,vserver in enumerate(vservers):
          if vserver['id'] == server.id:
            vserver['status_info'] = server.status
            vserver['ip'] = ', '.join(server.networks[nova_net]) if nova_net in server.networks else ''
            vserver['reported'] = True
            found_server = True
            break
        if found_server == False:
          get_vservers()
      for vserver in vservers:
        if vserver['reported'] == False:
          vserver['status_info'] = 'TERMINATED'
          vserver['cpu'] = 0 
          vserver['ram'] = 0
    except:
      print('[dashboard] error, could not call Openstack, trying again')

get_vservers() # so that the information about the servers is initially present.
vserver_refresher = threading.Thread(target=vserver_thread)
vserver_refresher.start()