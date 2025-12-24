import time
from myqueue import Queue    

# Lane queues
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
PRIORITY_LIMIT = 10


def read_input():
    """Read vehicle arrivals from input.txt"""
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()

        # Clear file after reading
        open("input.txt", "w").close()

        for road in lines:
            road = road.strip()
            if road in road_map:
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

    print("\nQueue Status")
    print("A:", AL1.size(),
          "B:", BL1.size(),
          "C:", CL1.size(),
          "D:", DL1.size(),
          "A-Priority:", AL2.size())

    # Priority handling
    if AL2.size() >= PRIORITY_LIMIT:
        print("Priority lane active")
        served = serve(AL2, AL2.size())
        time.sleep(served * TIME_PER_VEHICLE)

    else:
        print("Normal traffic flow")

        queues = [AL1, BL1, CL1, DL1]
        total = sum(q.size() for q in queues)

        if total == 0:
            print("No vehicles. Waiting...")
            time.sleep(1)
            continue

        # Serve at least 1 vehicle if traffic exists
        per_lane = max(1, total // len(queues))

        for q in queues:
            serve(q, per_lane)

        time.sleep(per_lane * TIME_PER_VEHICLE)

    time.sleep(1)
