from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPOk
import uuid
import datetime
import threading

import time
import queue
import requests
import socket

import transaction

import queue

from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql import text

from .models import (
    DBSession,
    MyModel,
    Message,
    DelMessage,
    )

messages = []

displayed_messages = []

deleted_messages = []

DBmb1 = queue.Queue()

@view_config(route_name='home', renderer='home.mako')
def my_view(request):
  global messages, displayed_messages

  messages = []
  displayed_messages = []

  query = "SELECT messages.* FROM messages LEFT JOIN \
    del_messages ON messages.msgid = del_messages.msgid \
    WHERE del_messages.msgid IS null"
  qmsg = DBSession.query(Message).from_statement(text(query)).all()

  for msg in qmsg:
    messages.append(msg.__dict__)
    displayed_messages.append(msg.__dict__)

  '''
  try:
    one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
  except DBAPIError:
    print('mistakes were made')
  '''
  return {'project': 'CRDT Note Taking',
          'messages': displayed_messages,
          'hostname': str(socket.gethostname())}

@view_config(route_name='compose')
def compose_view(request):
  global messages, displayed_messages

  msgfield = request.params['msgfield']

  msgid = str(uuid.uuid4())
  mbtimestamp = datetime.datetime.now().ctime()

  msg = {'msgid': msgid,#id <- msgid
         'content': msgfield, #content <- msg
         'timestamp': mbtimestamp#mbtimestamp < date
        }

  messages.append(msg)
  displayed_messages.append(msg)

  message = Message(msgid = msgid, content = msgfield, timestamp = mbtimestamp)
  DBSession.add(message)
  transaction.commit()

  return HTTPFound(location='/')

@view_config(route_name='delete')
def delete_view(request):
  global deleted_messages, displayed_messages

  msgid = request.params['msgid']

  mbtimestamp = datetime.datetime.now().ctime()

  deleted_messages.append({
    'msgid': msgid,
    'timestamp': mbtimestamp
    })
  del_displayed_msg(msgid)

  dmessage = DelMessage(msgid = msgid, timestamp = mbtimestamp)
  DBSession.add(dmessage)
  transaction.commit()
  
  return HTTPFound(location='/')

@view_config(route_name='apilist', renderer='json')
def api_list_view(request):
  return {'messages': displayed_messages}

@view_config(route_name='apidelete', renderer='json')
def api_delete_view(request):
  global deleted_messages, displayed_messages, DBdel

  msgid = request.params['id']

  mbtimestamp = datetime.datetime.now().ctime()

  deleted_messages.append({
    'msgid': msgid,
    'timestamp': mbtimestamp
    })
  del_displayed_msg(msgid)

  dmessage = DelMessage(msgid = msgid, timestamp = mbtimestamp)

  DBmb1.put(dmessage)

  #DBSession.add(dmessage)
  #transaction.commit()
  
  return {'status': 'ok'}

@view_config(route_name='apiinsert', renderer='json')
def api_insert_view(request):
  global messages, displayed_messages, DBins

  msgfield = request.params['content']

  msgid = str(uuid.uuid4())
  mbtimestamp = datetime.datetime.now().ctime()

  msg = {'msgid': msgid,#id <- msgid
         'content': msgfield, #content <- msg
         'timestamp': mbtimestamp#mbtimestamp < date
        }

  messages.append(msg)
  displayed_messages.append(msg)

  message = Message(msgid = msgid, content = msgfield, timestamp = mbtimestamp)
  DBmb1.put(message)

  #DBSession.add(message)
  #transaction.commit()

  return {'id': msgid}

#########
def del_displayed_msg(msid):
  global displayed_messages
  for message in displayed_messages:
    if message['msgid'] == msid:
      displayed_messages.remove(message)
      break

def pusdb():
  global DBins, DBdel

  while True:
    print('collecting DBs')
    ops = []
    for x in range(0,50):
      try:
        a = DBmb1.get(timeout=3)
        ops.append(a)      
      except:
        break

    for x in ops:
      DBSession.add(x)
    transaction.commit()
    print('pushing DBs')


db_thread = threading.Thread(target=pusdb)
db_thread.start()

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_tempo_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""