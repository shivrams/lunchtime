# -*- coding: utf-8 -*-
''' All config variables
'''
from os import environ
ENVIRONMENT_VAR_PREFIX = 'LUNCHTIME_'


class Config(object):
    ''' Class to wrap around config variables
    '''
    def __init__(self):
        ''' Parse os.environ and set all members. The environment variables can have the same
            format as the variable names below, but prefixed by LUNCHTIME_
        '''
        self.ALLOWED_SLACK_ROOMS = ['lunch', 'lunch-test']
        self.SLACK_REQUEST_TOKEN = ''
        self.INCOMING_WEBOOK_URL = ''
        for name, value in environ.iteritems():
            name = name.replace(ENVIRONMENT_VAR_PREFIX, '')
            if hasattr(self, name):
                setattr(self, name, value)
