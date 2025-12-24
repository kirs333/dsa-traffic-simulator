from myqueue import Queue

q = Queue(5)

q.enqueue(10)
q.enqueue(20)
q.enqueue(30)

q.display()

print("Dequeued:", q.dequeue())
print("Front element:", q.peek())

q.display()
