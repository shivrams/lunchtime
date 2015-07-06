''' Handles all slack incoming webhook integration for the lunchbot.
    Incoming webhooks are used in slack to send a message to the channel for all to see.
'''
import requests

WEBHOOK_MSG_NEW_ORDER_CREATED = '@everyone: New order created by {username}. \n\n {place}'
WEBHOOK_MSG_NOTIFY_PENDING_ORDERS = 'Please put your order in or back out via `/lunch out`'
WEBHOOK_MSG_ORDER_CANCELLED = 'The order below has been cancelled! \n\n{order}'
WEBHOOK_MSG_ORDER_FINISHED = 'The order below has been placed! \n\n{order}'


class IncomingWebhook(object):
    ''' Class that packages and sends the right http request to post a message
        to a slack channel that's visible to all
    '''
    def __init__(self, incoming_webhook_url):
        ''' Init accepts the webhook URL that we will send POST requests to
        '''
        self.incoming_webhook_url = incoming_webhook_url

    def post_simple_text(self, text):
        ''' Just send a simple POST request with a JSON payload matching webhook docs
        '''
        payload = {'text': text}
        return requests.post(self.incoming_webhook_url, data=payload)

    def on_new_order(self, **kwargs):
        ''' Incoming webhook actions needed when a new lunch order is created
        '''
        message = WEBHOOK_MSG_NEW_ORDER_CREATED.format(**kwargs)
        return self.post_simple_text(message)

    def on_cancel_order(self, order):
        ''' Send a message to everyone in the channel when an order is cancelled
        '''
        message = WEBHOOK_MSG_ORDER_CANCELLED.format(order=order)
        return self.post_simple_text(message)

    def on_finish_order(self, order):
        ''' Send a message to everyone in the channel when an order is finished
        '''
        message = WEBHOOK_MSG_ORDER_FINISHED.format(order=order)
        return self.post_simple_text(message)

    def on_notify_pending_orders(self, notify_message, notify_users):
        ''' Send a message mentioning pending order users with a special message from creator
        '''
        if not notify_message:
            notify_message = WEBHOOK_MSG_NOTIFY_PENDING_ORDERS

        notify_message = '{users} {message}'.format(users=notify_users, message=notify_message)
        return self.post_simple_text(notify_message)
