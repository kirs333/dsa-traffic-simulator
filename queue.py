class Queue:
    def __init__(self, size):
        self.size = size
        self.queue = []
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def is_full(self):
        return len(self.queue) == self.size
    
    def enqueue(self, item):
        if self.is_full():
            print("Queue is full")
            return
        self.queue.append(item)
    
    def dequeue(self):
        if self.is_empty():
            print("Queue is empty")
            return None
        return self.queue.pop(0)
    
    def peek(self):
        if self.is_empty():
            return None
        return self.queue[0]
    
    def display(self):
        print(self.queue)
