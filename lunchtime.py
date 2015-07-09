# -*- coding: utf-8 -*-
''' This is where all the action happens. Running this module fires up
    the webserver listening for requests from slack

    Additionally also
'''
import cherrypy
import logging

from config import Config
from slack.incoming_webhook import IncomingWebhook
from utils import require_in_self
import responses

conf = Config()


class LunchTimeCommandHandler(object):
    ''' Class containing all methods to handle different
        commands as well as the dispatcher
    '''
    command_handlers = None

    def __init__(self):
        ''' Map all commands to command handlers
        '''
        self.current_order = {}
        self.current_order_items = {}

        self.command_handlers = {
            '': self._open_orders_command,
            'where': self._open_orders_command,
            'help': self._help_command,
            'new': self._new_command,
            'in': self._in_command,
            'out': self._out_command,
            'order': self._order_command,
            'cancel': self._cancel_order_command,
            'ordered': self._finish_order_command,
            'finish': self._finish_order_command,
            'finished': self._finish_order_command,
            'placed': self._finish_order_command,
            'list': self._current_order_status_command,
            'status': self._current_order_status_command,
            'notify': self._notify_pending_orders_command,
        }
        self.incoming_webhook = IncomingWebhook(conf.INCOMING_WEBOOK_URL)

    @property
    def current_order_creator(self):
        ''' Returns the username of the creator of the current order
        '''
        if not self.current_order:
            return ''

        return self.current_order['username']

    @property
    def pending_order_users(self):
        ''' Returns a space separated string of usernames that are "in" but havent placed an order
        '''
        pending_users = []
        for username, order in self.current_order_items:
            if not order:
                pending_users.append(username)

        return ' '.join(pending_users)

    @property
    def formatted_current_order(self):
        ''' Returns the current order in a formatted message
        '''
        if self.current_order:
            return 'Current order for {place} created by {username}\n\n'.format(
                **self.current_order
            )
        else:
            return 'Currently no open orders.'

    @property
    def formatted_current_order_items(self):
        ''' Just takes the current self.current_order_items and formats it properly
            into a string message
        '''

        formatted_order = self.formatted_current_order
        for username, order in self.current_order_items:
            if not order:
                # No order put in yet
                order = 'Waiting on an order...'
            formatted_order += '{username}: {order}\n'.format(
                username=username,
                order=order,
            )

        return formatted_order

    def handle(self, command, username):
        ''' Dispatcher that calls different methods based on the
            command
        '''
        command_arg = ''
        if ' ' in command:
            # Break command into command + command arguments
            command, command_arg = command.split(' ', 1)

        command_handler = self.command_handlers.get(command)
        if command_handler:
            return command_handler(username, command_arg)
        else:
            return None

    def _reset_order(self):
        ''' Empties out the current order and current order items
        '''
        self.current_order = {}
        self.current_order_items = {}

    def _open_orders_command(self):
        ''' Returns information about the current open order.
        '''

        if self.current_order:
            return responses.MSG_SUCCESS_OPEN_ORDERS.format(**self.current_order)
        else:
            return responses.MSG_FAIL_OPEN_ORDERS

    def _help_command(self, *args):
        ''' Someone wants help! Respond with the full help text
        '''

        return responses.MSG_HELP

    def _new_command(self, username, lunch_place):
        ''' New lunch order at 'lunch_place' from 'username'
        '''
        if self.current_order:
            return responses.MSG_FAIL_NEW_EXISTING_ORDER

        logging.info('New order for %s created by %s', lunch_place, username)

        # There is no existing order, let's create a new one
        self.current_order['username'] = username
        self.current_order['place'] = lunch_place

        # Whoever created the order is automatically in
        self.current_order_items[username] = ''

        # Using the incoming web hook, send a message to the channel mentioning everyone
        self.incoming_webhook.on_new_order(username=username, place=lunch_place)

        return responses.MSG_SUCCESS_NEW_ORDER_CREATED

    @require_in_self(['current_order'])
    def _in_command(self, username, *args):
        ''' Just username letting us know that they're participating in the order.
            Essentially grabbing a place.
        '''
        if username in self.current_order_items:
            return responses.MSG_FAIL_ALREADY_IN.format(order=self.current_order_items[username])

        logging.info('%s is in', username)
        self.current_order_items[username] = ''

        return responses.MSG_SUCCESS_IN

    @require_in_self(['current_order'])
    def _out_command(self, username, *args):
        ''' Just username letting us know that they're out of the order.
            Essentially backing out if they were previous in/ordered
        '''
        if username not in self.current_order_items:
            return responses.MSG_FAIL_OUT_WITHOUT_IN

        logging.info('%s is out', username)
        del self.current_order_items[username]

        return responses.MSG_SUCCESS_OUT

    @require_in_self(['current_order'])
    def _order_command(self, username, order):
        ''' Just username letting us know what they want to order.
        '''
        logging.info('%s wants %s', username, order)
        self.current_order_items[username] = order
        return responses.MSG_SUCCESS_ORDER_PUT_IN

    @require_in_self(['current_order_items'])
    def _cancel_order_command(self, username, *args):
        ''' Cancelling the entire order. Can only be triggered by the user who created one.
            Also, sends a message to the entire channel confirming order cancellation.
        '''
        if username != self.current_order_creator:
            return responses.MSG_FAIL_ONLY_CREATOR_CANCELS

        logging.info('%s is cancelled', self.formatted_current_order)

        self.incoming_webhook.on_cancel_order(order=self.formatted_current_order)
        self._reset_order()
        return responses.MSG_SUCCESS_CANCEL_ORDER

    @require_in_self(['current_order_items'])
    def _finish_order_command(self, username, *args):
        ''' Finishing the entire order. Can only be triggered by the user who created one.
            Also, sends a message to the entire channel confirming order.
        '''
        if username != self.current_order_creator:
            return responses.MSG_FAIL_ONLY_CREATOR_FINISHES

        logging.info('%s is placed', self.formatted_current_order)
        self.incoming_webhook.on_finish_order(order=self.formatted_current_order)
        self._reset_order()
        return responses.MSG_SUCCESS_FINISH_ORDER

    @require_in_self(['current_order'])
    def _current_order_status_command(self, *args):
        ''' Returns a detailed message for current order and participants along with
            order for each participant.
        '''
        return self.formatted_current_order

    @require_in_self(['current_order_items'])
    def _notify_pending_orders_command(self, username, notify_message):
        ''' Uses the webhook
        '''
        if username != self.current_order_creator:
            return responses.MSG_FAIL_ONLY_CREATOR_NOTIFIES

        if not self.pending_order_users:
            return responses.MSG_FAIL_NONE_PENDING_TO_NOTIFY

        # FIXME Send a DM to all these users instead of webhook message
        self.incoming_webhook.on_notify_pending_orders(
            message=notify_message,
            users=self.pending_order_users,
        )

        return responses.MSG_SUCCESS_NOTIFY_PENDING_ORDERS


class LunchTime(object):
    ''' Handler hit whenever /lunch is entered into digg slack
    '''
    def __init__(self, command_handler):
        ''' Initialize the command handler provided
        '''
        self.command_handler = command_handler

    @cherrypy.expose
    def lunch(self, **kwargs):
        ''' Inspect post params in the request and handle based
            on the text
        '''
        # Check if the right token is in the request
        request_token = kwargs.get('token')
        if request_token != conf.SLACK_REQUEST_TOKEN:
            invalid_request = True

        channel_name = kwargs.get('channel_name')
        if channel_name not in conf.ALLOWED_SLACK_ROOMS:
            # Only works in the lunch channel
            invalid_request = True

        if invalid_request:
            raise cherrypy.HTTPError(
                403,
                message="Invalid request. Are you in the #lunch channel?"
            )

        command = kwargs.get('text', '')
        command = command.lower().strip()
        username = kwargs.get('user_name')

        response = self.command_handler.handle(command, username)
        if response is None:
            raise cherrypy.HTTPError(
                403,
                message="Invalid request. Are you in the #lunch channel?"
            )
        return response

    @staticmethod
    def plain_text_error_page(status, message, traceback, version):
        ''' Used for plain text error page
        '''
        cherrypy.response.headers['content-type'] = 'text/plain'
        return message

if __name__ == '__main__':
    command_handler = LunchTimeCommandHandler()
    cherrypy.config.update({
        'server.socket_port': conf.CHERRYPY_PORT,
        'error_page.403': LunchTime.plain_text_error_page,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],
    })
    cherrypy.quickstart(LunchTime(command_handler))
