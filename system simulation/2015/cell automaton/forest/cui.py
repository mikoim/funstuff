__author__ = 'Eshin Kunishima'
__license__ = 'MIT'

from forest import Forest

f = Forest()
f.loads(open('default2.txt', mode='r').read())
print(f.dumps())
for t in range(1800):
    f.next_generation()
    print(f.dumps())
