import time


def with_exception(exc):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            try:
                response = f(*args, **kwargs)
            except Exception as e:
                raise exc from e
            return response
        return wrapped
    return inner_decorator


def with_debug_time(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        print("{0:<15} | Exec time : {1:.8}".format(func.__name__, t1 - t0))
        return result

    return wrapper
