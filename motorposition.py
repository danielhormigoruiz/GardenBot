#!/usr/bin/env python

import redis
import os
from time import time, sleep
import json
import requests


def log(message, message_type):
    'Send a message to the log.'
    try:
        os.environ['FARMWARE_URL']
    except KeyError:
        print(message)
    else:
        log_message = '[motors-position] ' + str(message)
        headers = {
            'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
            'content-type': "application/json"}
        payload = json.dumps(
            {"kind": "send_message",
             "args": {"message": log_message, "message_type": message_type}})
        requests.post(os.environ['FARMWARE_URL'] + 'celery_script',
                      data=payload, headers=headers)

def get_information():
  
  try:
    r = redis.Redis()
    device_current_position_x = r.get('BOT_STATUS.location_data.position.x')
    device_current_position_y = r.get('BOT_STATUS.location_data.position.y')
    device_current_position_z = r.get('BOT_STATUS.location_data.position.z')
    message = "X{0}, Y{1}, Z{2}".format(device_current_position_x, device_current_position_y, device_current_position_z)
    print("Position: " + message)
    
  except:
    log(message, "error")

if __name__ == '__main__':      
  get_information()  

