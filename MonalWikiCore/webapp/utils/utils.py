
#currently for frontend endpoint only
def pre_endpoint_run(endpoint_func):
    """

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        print ("in pre_endpoint_run")
        print ("request =",  request)
        return func(*args, **kwargs)

    return wrapper



