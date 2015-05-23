# -*- coding: utf-8 -*-
''' This is where all the action happens. Running this module fires up
    the webserver listening for requests from slack

    Additionally also
'''
import cherrypy
from config import Config

conf = Config()

CURRENT_ORDER = {}
CURRENT_ORDER_ITEMS = []

ALLOWED_COMMANDS = [
    'new',  # create a new lunch order
]


class LunchTime(object):
    ''' Handler hit whenever /lunch is entered into digg slack
    '''
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def lunch(self):
        ''' Inspect post params in the request and handle based
            on the text
        '''
        return {'text': 'Hello world!'}

if __name__ == '__main__':
    cherrypy.quickstart(LunchTime())
