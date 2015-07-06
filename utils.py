''' Contains all the helpers
'''

from functools import wraps


def require_in_self(required_args=[]):
    '''
    Meant to be a decorator to apply on instance methods in a class where each of the required
    args is the instance variable name, and its corresponding value is checked for
    boolean trueness

    '''
    def decorator(f):
        @wraps(f)
        def test_boolean_trueness(self, *args, **kwargs):
            arg_values = []
            for arg in required_args:
                arg_value = getattr(self, arg, None)
                arg_values.append(arg_value)

            if not all(arg_values):
                return 'Missing some required arguments. Maybe try `/lunch help`?'

            return f(*args, **kwargs)

        return test_boolean_trueness
    return decorator
