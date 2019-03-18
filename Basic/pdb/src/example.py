# import pdb
from ipdb import launch_ipdb_on_exception
#import ipdb

def calc(operator, num1, num2):
    # pdb.set_trace()
    if operator is '+':
        return num1 + num2
    elif operator is '-':
        return num1 - num2
    elif operator is '*':
        return num1 * num2
    else:
        return num1 / num2

# pdb.set_trace()
#ipdb.set_trace()

with launch_ipdb_on_exception():
    ret = 10 / 0

num1 = 100
# ipdb.set_trace(context=5)
num2 = 5


result = calc('*', num1, num2)
#ipdb.pm()

print(result)

