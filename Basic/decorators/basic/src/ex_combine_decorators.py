from functools import wraps


def decorator_1(func):
    @wraps(func)
    def wrapper_1(*args, **kwargs):
        print('Begin decorator_1')
        func(*args, **kwargs)
        print('End decorator_1')
        return 1
    return wrapper_1

def decorator_2(func):
    @wraps(func)
    def wrapper_2(*args, **kwargs):
        print('Begin decorator_2')
        func(*args, **kwargs)
        print('End decorator_2')
        return 2
    return wrapper_2


def composed(*desc):
    def wrapper(func):
        f = func
        for d in desc:
            f = d(f)
        return f
    return wrapper
    

@composed(decorator_2, decorator_1)
def test():
    """This is test function."""
    print('I am test function of python.')


print(test.__doc__)
print()
test()