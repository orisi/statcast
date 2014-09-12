#!/usr/bin/python

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
      print decoded_body
      if not verify(req['body'], req['signature'], req['source']):
        continue

      decoded_results.append(req)
    except:
      continue

  data['results'] = decoded_results
  return data


#msgs = json.loads(getMessages()['results'])
#print msgs

msgs = getMessages()['results']


import time

import ast

for msg in msgs:

  print "[ Source ]"
  print msg['source']
  
  print "[ Published Time ]"
  ago =  int(time.time()) - 7200 - int(msg['epoch'])
  print str(ago) + " seconds ago"
   
  ff = eval(msg['body'])
  
  
  try:  
    if ff['operation']: 
      print "[ Operation ]"
      print ff['operation'] 
  except:
    pass
  
  try:
    if ff['message_id']: 
      print "[ Message Id ]"
      print ff['message_id'] 
  except:
    pass
    
 
  try:  
    if ff['comment']: 
      print "[ Comment ]"
      print ff['comment'] 
  except:
    pass
  
  try:
    if ff['contract_id']: 
      print "[ Contract Id ]"
      print ff['contract_id'] 
  except:
    pass
  
  try:
    if ff['in_reply_to']: 
      print "[ In Reply To ]"
      print ff['in_reply_to'] 
  except:
    pass
    
  
  print 
  print  
  print
      
