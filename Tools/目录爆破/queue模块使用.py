import queue
import threading
'''
q = queue.Queue()
q.put('a')
q.put('b')
print(q.get())
print(q.get())
for i in range(10):
    q.put(i)

while not q.empty():
    print(q.get())
'''
q = queue.Queue()
for i in range(30):
    q.put(i)
def test(q):
    while not q.empty():
        threadname = threading.current_thread().getName()
        print(threadname, q.get())
for i in range(3):
    t = threading.Thread(target=test, args=(q, ))
    t.start()
