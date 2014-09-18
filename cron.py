#!/usr/bin/python

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statcast.settings")

from monitor.models import *

import requests
import json
import base64



from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

headers = {'content-type': 'application/json'}
def decode_data(data):
        return base64.decodestring(data)

def code_data(data):
        base64.encodestring(data)

def sign(message, priv_b64):
  priv = base64.decodestring(priv_b64)
  key = RSA.importKey(priv)
  signer = PKCS1_v1_5.new(key)

  digest = SHA256.new()
  digest.update(message)

  sign = signer.sign(digest)

  return base64.encodestring(sign)

def verify(message, signature_b64, pub_b64):
  pub = base64.decodestring(pub_b64)
  signature = base64.decodestring(signature_b64)
  key = RSA.importKey(pub)
  signer = PKCS1_v1_5.new(key)
  digest = SHA256.new()
  digest.update(message)
  if signer.verify(digest, signature):
    return True
  return False




def getMessages():
  url = 'http://54.77.58.8?format=json'
  r = requests.get(url)
  data = json.loads(r.text)

  decoded_results = []
  for req in data['results']:
    try:
      decoded_body = decode_data(req['body'])
      req['body'] = decoded_body
      #print decoded_body
      if not verify(req['body'], req['signature'], req['source']):
        continue

      decoded_results.append(req)
    except:
      continue

  data['results'] = decoded_results
  return data


#msgs = json.loads(getMessages()['results'])
#print msgs

#msgs = getMessages()['results']


import time




# myapp/cron.py
import cronjobs

@cronjobs.register
def downloader():
    
    
    msgs = getMessages()['results']
      
    
    for msg in msgs:

      print "[ Source ]"

      #if not msg['source']: msg['source'] = "uknown"
      print msg['source']

      print "[ Published Time ]"
      ago =  int(time.time()) - 7200 - int(msg['epoch'])
      print str(ago) + " seconds ago"

      ff = eval(msg['body'])


      try:
        if ff['operation']:
          print "[ Operation ]"
          print ff['operation']
        else:
          ff['operation'] = ""
      except:
        pass

      try:
        if ff['message_id']:
          print "[ Message Id ]"
          print ff['message_id']
        else:
          ff['message_id'] = ""
      except:
          ff['message_id'] = ""

          pass


      try:
        if msg['return_address']:
          print "[ Return Address ]"
          print msg['return_address']
        else:
          msg['return_address'] = ""
      except:
          msg['return_address'] = ""

          pass




      try:
        if ff['comment']:
          print "[ Comment ]"
          print ff['comment']
        else:
          ff["No comment."]
      except:
        ff['comment'] = "No comment."

        pass

      try:
        if ff['contract_id']:
          print "[ Contract Id ]"
          print ff['contract_id']

        else:
          ff['contract_id'] = "init"
      except:
        ff['contract_id'] = "init"
      pass

      try:
        if ff['in_reply_to']:
          print "[ In Reply To ]"
          print ff['in_reply_to']
        else:
          ff['in_reply_to'] = ""
      except:
          ff['in_reply_to'] = ""
          pass


      try:
        if msg['signature']:
          print "[ Signature ]"
          print msg['signature']
        else:
          msg['signature'] = ""
      except:
          msg['signature'] = ""
          pass


      try:
        if ff['locktime']:
          print "[ Locktime ]"
          print ff['locktime']
        else:
          ff['locktime'] = ""
      except:
          ff['locktime'] = ""
          pass



      ping, created = Ping.objects.get_or_create(source=msg['source'])

      #if created:
      #  ping.update(published_time=msg['epoch'])
      #Belse:
      #B  print ping
      #  ping.update(published_time=msg['epoch'])
      
      Ping.objects.filter(source=msg['source']).update(published_time=msg['epoch'])
          
      
      Monitor.objects.get_or_create(

        source=msg['source'],
        contract_id=ff['contract_id'],
        message_id=ff['message_id'],
        operation=ff['operation'],
        published_time = msg['epoch'],

        comment=ff['comment'],
        in_reply_to = ff['in_reply_to'],
        return_address = msg['return_address'],
        locktime = ff['locktime'],


      )
  
  
      print
      print
      print



while True:
    downloader()
    time.sleep(7)
    
