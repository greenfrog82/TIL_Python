from __future__ import print_function
import threading
from multiprocessing.pool import ThreadPool

print_lock = threading.Lock() # Without this, you will get messy output

def p(*args):
  with print_lock:
    print(threading.current_thread().name, *args)

def generate_items():
  for i in range(4):
    p('----- GENERATE_ITEMS {}'.format(i))
    yield i

def square(x):
  result = x * x
  p('square {} = {}'.format(x, result))
  return result

def main():
  p('main')
  pool = ThreadPool(10)
  for result in pool.imap_unordered(square, generate_items()):
    p('main, for loop body', result)
  pool.close()
  pool.join()

if __name__ == '__main__':
  main()
