import time
from queue import Queue

AL1 = Queue()
BL1 = Queue()
CL1 = Queue()
DL1 = Queue()

AL2 = Queue()

road_map = {
    "A": AL1,
    "B": BL1,
    "C": CL1,
    "D": DL1
}

RED = 1
GREEN = 2

current_light = RED
TIME_PER_VEHICLE = 1


def read_input():
    """Read vehicle arrivals from input.txt"""
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()
        open("input.txt", "w").close()  # clear file

        for road in lines:
            road = road.strip()
            if road in road_map:
                road_map[road].enqueue("V")
    except FileNotFoundError:
        pass


def serve_queue(queue, vehicles):
    """Serve vehicles from a queue"""
    served = 0
    while not queue.is_empty() and served < vehicles:
        queue.dequeue()
        served += 1
    return served


while True:
    read_input()

    print("\nCurrent Queue Sizes:")
    print("AL1:", AL1.size(), "BL1:", BL1.size(),
          "CL1:", CL1.size(), "DL1:", DL1.size(),
          "AL2 (Priority):", AL2.size())

    if AL2.size() > 10:
        print("Priority condition active: Serving AL2")
        current_light = GREEN
        served = serve_queue(AL2, AL2.size())
        time.sleep(served * TIME_PER_VEHICLE)

    else:
        print("Normal condition: Fair serving")
        queues = [AL1, BL1, CL1, DL1]
        total = sum(q.size() for q in queues)

        if total > 0:
            avg = total // len(queues)
            current_light = GREEN

            for q in queues:
                serve_queue(q, avg)

            time.sleep(avg * TIME_PER_VEHICLE)

    current_light = RED
    time.sleep(1)
