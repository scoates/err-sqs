#!/usr/bin/env python

import os
import sys
import time
import boto3

sqs = boto3.resource('sqs')

channel = "#" + sys.argv[1]

queue = sqs.get_queue_by_name(QueueName=os.environ['QUEUE_NAME'])
queue.send_message(
    MessageAttributes={
        'channel': {
            'StringValue': channel,
            'DataType': 'String'
        }
    },
    MessageBody=" ".join(sys.argv[2:]),
    MessageGroupId=str(time.time())
)
