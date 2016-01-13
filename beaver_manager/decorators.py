from threading import Thread


def async(f):
    """Decorator that will make any function asynchronus"""
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
