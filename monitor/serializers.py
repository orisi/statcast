from django.contrib.auth.models import User, Group
from rest_framework import serializers

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import base64
import binascii

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

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

from monitor.models import Monitor, Ping


#    source = models.CharField( max_length = 255, blank=True)
#    contract_id = models.CharField( max_length = 255, blank=True)
#    published_time = models.IntegerField( max_length = 255 )
#    signature = models.CharField( max_length = 255 )
#    operation = models.CharField( max_length = 255 )
#    return_address = models.CharField( max_length = 255 )
#    in_reply_to = models.CharField( max_length = 255 )
#    locktime = models.CharField( max_length = 255 )
#    pubkey_list = models.CharField( max_length = 255 )
#    message_id = models.CharField( max_length = 255 )
#    timestamp = models.DateTimeField(auto_now_add=True)

class MonitorSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Monitor
        fields = ('source','contract_id','published_time','signature','operation','return_address','in_reply_to','locktime','message_id')

class PingSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Monitor
        fields = ('source','published_time')


