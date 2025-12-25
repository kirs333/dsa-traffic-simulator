import time
from myqueue import Queue   

# Incoming lanes
AL1 = Queue()
BL1 = Queue()
CL1 = Queue()
DL1 = Queue()

# Priority lane
AL2 = Queue()

road_map = {
    "A": AL1,
    "B": BL1,
    "C": CL1,
    "D": DL1
}

TIME_PER_VEHICLE = 1


def read_input():
    """Reads vehicle arrivals from file and pushes them into queues"""
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()

        open("input.txt", "w").close()  # clear after reading

        for road in lines:
            road = road.strip()
            if road == "A":
                AL2.enqueue("V")      # A goes to priority lane
            elif road in road_map:
                road_map[road].enqueue("V")
    except FileNotFoundError:
        pass


def serve(queue, count):
    """Serve vehicles from a queue"""
    served = 0
    while not queue.is_empty() and served < count:
        queue.dequeue()
        served += 1
    return served


while True:
    read_input()

    print("\nQueue Status:")
    print(
        "AL1:", AL1.size(),
        "BL1:", BL1.size(),
        "CL1:", CL1.size(),
        "DL1:", DL1.size(),
        "| AL2 (Priority):", AL2.size()
    )

    # Priority condition
    if AL2.size() > 10:
        print("Priority active → Serving AL2")
        served = serve(AL2, AL2.size())
        time.sleep(served * TIME_PER_VEHICLE)

    else:
        print("Normal condition → Fair serving")

        normal_queues = [AL1, BL1, CL1, DL1]
        total_vehicles = sum(q.size() for q in normal_queues)

        if total_vehicles > 0:
            avg = max(1, total_vehicles // len(normal_queues))

            for q in normal_queues:
                serve(q, avg)

            time.sleep(avg * TIME_PER_VEHICLE)

    time.sleep(1)
