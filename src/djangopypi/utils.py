import logging


def debug(func):
    # @debug is handy when debugging distutils requests
    def _wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logging.exception("@debug")
    return _wrapped
