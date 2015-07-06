''' Module containing all the slash command responses.
'''
MSG_FAIL_NEW_EXISTING_ORDER = ('Cannot place a new order since there is already'
                               ' an existing order')
MSG_SUCCESS_NEW_ORDER_CREATED = 'Congratulations! Your new order has been created!'

MSG_SUCCESS_OPEN_ORDERS = ('Current open order from {place} created by {username}.\n\n '
                           'Try `/lunch help` to see how you can join in!')
MSG_FAIL_OPEN_ORDERS = 'No open orders. Try `/lunch help` to see how you can create one.'

MSG_FAIL_ALREADY_IN = "You're already in the order! Current order is '{order}'"
MSG_SUCCESS_IN = "You're in! Decide on what you want and say `/lunch order this is what i want`"

MSG_FAIL_OUT_WITHOUT_IN = 'Cannot go out of an order that you were never in.'
MSG_SUCCESS_OUT = "Youuuuuu're OUT!"

MSG_SUCCESS_ORDER_PUT_IN = 'Your order is now in the system! *stomach growls*'

MSG_FAIL_ONLY_CREATOR_CANCELS = 'This order can only be cancelled by its creator'
MSG_FAIL_ONLY_CREATOR_FINISHES = 'This order can only be finished by its creator'

MSG_SUCCESS_CANCEL_ORDER = 'This order has been successfully cancelled'
MSG_SUCCESS_FINISH_ORDER = 'This order has been successfully finished'

MSG_FAIL_ONLY_CREATOR_NOTIFIES = 'Only the creator can notify the people we are waiting on.'
MSG_FAIL_NONE_PENDING_TO_NOTIFY = 'Everyone has put their order in. Ready to go!'
MSG_SUCCESS_NOTIFY_PENDING_ORDERS = 'You tell em!'

MSG_HELP = (
    'Welcome to lunchbot! lunchbot is designed to help you organize lunch orders via the `/lunch` '
    'command. A list of commands with examples is below to help you get started. \n'
    '`/lunch help`: Brings up this help text\n'
    '`/lunch` or `/lunch where`: Responds with the current open order info\n'
    '`/lunch new <text_with_link_here>`: Creates a new order and notifies the channel\n'
    '`/lunch in`: Puts you in the order, and is usually followed by `/lunch order`\n'
    '`/lunch order <what_you_want>`: Puts your order in for the creator\n'
    '`/lunch out`: Removes you from the order\n'
    '`/lunch cancel`: Cancels the open order, can only be initiated by the creator\n'
    '`/lunch ordered`: Marks the open order as placed, can only be initiated by the creator\n'
    '`/lunch list(or)status`: Lists the current order and which items have been requested\n'
    '`/lunch notify`: Notifies those who are in, but havent placed the order yet.\n\n'
    'Report any bugs/ideas to shivram@digg.com'

)
