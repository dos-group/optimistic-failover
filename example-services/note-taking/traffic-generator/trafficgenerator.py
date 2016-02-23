import threading
import time
import requests
import random
import uuid
import datetime

# change to the address of your installation
MB1 = 'http://localhost:6543'

# second address for consistency tests
# MB2 = 'http://192.168.4.186:6543'

WORDS = (
  'soamed',
  'tub',
  'cit',
  'yolo',
  'swag',
  'peanut',
  'butter',
  'jelly',
  'time'
  )

messages = []

mb1ops = []
mb1messages = []

mb2ops = []
mb2messages = []

def main():
  global messages, mb1ops, mb2ops

  for x in range(0,3000):
    msg = None

    if len(messages) > 1000:

      msg = messages.pop(random.randint(0,len(messages) - 1))

      mb1ops.append(
        {'op' : 'delete',
        'iid': msg['iid']}
        )
        

      mb2ops.append(
        {'op' : 'delete',
        'iid': msg['iid']}
        )
        

    elif len(messages) > 10:
      if random.randint(0,1):
        msg = build_message()
        messages.append(msg)

        mb1ops.append(
          {'op' : 'insert',
          'iid': msg['iid'],
          'msg': msg['msg']}
          )
          

        mb2ops.append(
          {'op' : 'insert',
          'iid': msg['iid'],
          'msg': msg['msg']}
          )
          


      else:
        msg = messages.pop(random.randint(0,len(messages) - 1))

        mb1ops.append(
          {'op' : 'delete',
          'iid': msg['iid']}
          )
          

        mb2ops.append(
          {'op' : 'delete',
          'iid': msg['iid']}
          )
          

    else:
      msg = build_message()
      messages.append(msg)

      mb1ops.append(
        {'op' : 'insert',
        'iid': msg['iid'],
        'msg': msg['msg']}
        )
        

      mb2ops.append(
        {'op' : 'insert',
        'iid': msg['iid'],
        'msg': msg['msg']}
        )
        

  print('build complete')
  print('sending messages')

  send_messagemb1()

  #mb1_thread = threading.Thread(target=send_messagemb1)
  #mb1_thread.start()

  #mb2_thread = threading.Thread(target=send_messagemb2)
  #mb2_thread.start()



def build_message():

  msglen = random.randint(1,10)
  msgcontent = []

  for x in range(msglen):
    msgcontent.append(random.choice(WORDS))

  msg = {
    'msg': ' '.join(msgcontent),
    'iid': str(uuid.uuid4())
  }

  return msg

def send_messagemb1():
  global mb1ops, mb1messages
  responses = []

  sstart = datetime.datetime.now()
  while len(mb1ops):
    op = mb1ops.pop(0)

    if op['op'] == 'insert':

      try:
        a = datetime.datetime.now()
        data = requests.post(MB1+'/api/insert',data={'content': op['msg']},timeout=2)
        eid = data.json()['id']
        data.connection.close()
        b = datetime.datetime.now()
        c = b - a
        responses.append(c)
        print ('insert answer: ', c.total_seconds())

        mb1messages.append({'iid': op['iid'], 'eid': eid})
      except:
        print('[traffig-generator] error, could not call MB1, trying again')
        time.sleep(3)
        mb1ops.insert(0,op)
    else: 
      try:
        eid = get_eid(op['iid'],mb1messages)
        if eid == None:
          mb1ops.append(op)
          continue
        a = datetime.datetime.now()
        data = requests.post(MB1+'/api/delete',data={'id': eid},timeout=2)
        data.connection.close()
        b = datetime.datetime.now()
        c = b - a
        responses.append(c)
        print ('delete answer: ', c.total_seconds())
      except:
        print('[traffig-generator] error, could not call MB1, trying again')
        time.sleep(3)
        mb1ops.insert(0,op)

  sstop = datetime.datetime.now()

  print('overall sending time: ', (sstop - sstart).total_seconds())

  counter = responses[0]      
  for x in responses:
    counter = counter + x
  timer = counter / len(responses)
  print('average response time: ',timer.total_seconds())

'''
def send_messagemb2():
  global mb2ops, mb2messages
  while len(mb2ops):
    op = mb2ops.pop(0)

    if op['op'] == 'insert':
      try:
        data = requests.post(MB2+'/api/insert',data={'content': op['msg']})
        eid = data.json()['id']
        data.connection.close()

        mb2messages.append({'iid': op['iid'], 'eid': eid})
      except:
        print('[traffig-generator] error, could not call MB2, trying again')
        time.sleep(3)
        mb2ops.insert(0,op)
    else: 
      try:
        eid = get_eid(op['iid'],mb2messages)
        if eid == None:
          mb2ops.append(op)
          continue
        data = requests.post(MB2+'/api/delete',data={'id': eid})
        data.connection.close()
      except:
        print('[traffig-generator] error, could not call MB2, trying again')
        time.sleep(3)
        mb2ops.insert(0,op)
'''

def get_eid(iid, MB):
  for mapping in MB:
    if mapping['iid'] == iid:
      return mapping['eid']
  return None

#############################################

if __name__ == "__main__":
  main()
