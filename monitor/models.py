from django.db import models
from django.core.exceptions import ValidationError

import uuid # from http://zesty.ca/python/uuid.html
import base64
import datetime

def to_native(value):
    """ Return epoch time for a datetime object or ``None``"""
    import time
    try:
       return int(time.mktime(value.timetuple()))
    except (AttributeError, TypeError):
       return None




def fetch_code(custom_string="CODE_"):
    """
    usage:
    fetch_code()
    fetch_code(custom_string="KEY_")

    """
    b64uid = '00000000'


    uid = uuid.uuid4()
    b64uid = base64.b64encode(uid.bytes,'-_')

    code = b64uid[0:6]
    return custom_string+code

# Create your models here.
class Monitor( models.Model ):
    """
    Model for storing `messages`
    """

    source = models.CharField( max_length = 255, blank=True)
    contract_id = models.CharField( max_length = 255, blank=True)
    published_time = models.IntegerField( max_length = 255 )
    signature = models.CharField( max_length = 255 )
    operation = models.CharField( max_length = 255 )
    return_address = models.CharField( max_length = 255 )
    in_reply_to = models.CharField( max_length = 255 )
    locktime = models.CharField( max_length = 255 )
    message_id = models.CharField( max_length = 255 )
    comment = models.CharField( max_length = 255 )
    timestamp = models.DateTimeField(auto_now_add=True)
    

    