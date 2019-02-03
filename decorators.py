"""Various decorators for the project weatherapp
"""

import inspect
import time


def delay_execute(sec=1):
    """ Waits a given number of seconds before calling the function.
        The default is 1 second. 
    """

    def delay(func):
        def wrapper(*args, **kwargs):
            time.sleep(sec)
            return func(*args, **kwargs)

        return wrapper

    return delay


def execute_time(func):
    """Prints the execution time.
    """

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        run_time = time.perf_counter() - start_time
        print(f"Finished function in {run_time:.4f} secs")
        # print(f"Finished {func.__name__} in {run_time:.4f} secs")

        return result

    return wrapper


def get_args(func):
    """ Getting the names and values  of the incomin
        parameters of the function
    """

    def wrapper(*args, **kwargs):
        bound_args = inspect.signature(func).bind(*args, **kwargs)
        bound_args.apply_defaults()
        args_func = dict(bound_args.arguments)
        print("-" * 60)
        print(f"The function {func.__name__!r} accepts the parameters:\n")
        for key in args_func:
            print(f'{key}: {args_func[key]}')
        print("-" * 60, end='\n\n')

        return func(*args, **kwargs)

    return wrapper
