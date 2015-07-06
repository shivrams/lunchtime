# -*- coding: utf-8 -*-
''' All config variables
'''
from os import environ


class Config(object):
    ''' Class to wrap around config variables
    '''
    def __init__(self):
        ''' Parse os.environ and set all members
        '''
        self.SLACK_REQUEST_TOKEN = ''
        self.INCOMING_WEBOOK_URL = ''
        for name, value in environ.iteritems():
            if hasattr(self, name):
                setattr(self, name, value)


SLACK_REQUEST_TOKEN = "3z5volAl8eeT7RwYCy7XePoH"
INCOMING_WEBOOK_URL = "https://hooks.slack.com/services/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"
