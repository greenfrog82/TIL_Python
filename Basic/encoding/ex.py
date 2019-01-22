# encoding: utf-8
import sys
print sys.getdefaultencoding()

s = '파이썬'
u = u'파이썬'

print type(s)
print type(u)

# print s == u
# print s.decode('utf-8') == u
print s.decode('utf-8').encode('utf-8')
