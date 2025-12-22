import time
from myqueue import Queue 

# Incoming lane queues
AL1 = Queue()
BL1 = Queue()
CL1 = Queue()
DL1 = Queue()

# Priority
AL2 = Queue()

road_map = {
    "A": AL1,
    "B": BL1,
    "C": CL1,
    "D": DL1
}


RED = 1
GREEN = 2

TIME_PER_VEHICLE = 1


light_queue = ["A", "B", "C", "D"]
current_light = light_queue[0]


def read_input():
    """Read vehicle arrivals from input.txt"""
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()
        open("input.txt", "w").close()

        for road in lines:
            road = road.strip()
            if road in road_map:
                road_map[road].enqueue("V")

                # Road A lane 2 is priority
                if road == "A":
                    AL2.enqueue("V")

    except FileNotFoundError:
        pass


def serve_queue(queue, vehicles):
    """Serve given number of vehicles from a queue"""
    served = 0
    while not queue.is_empty() and served < vehicles:
        queue.dequeue()
        served += 1
    return served


def next_light():
    """Rotate traffic light (Day 4 logic)"""
    global current_light
    light_queue.append(light_queue.pop(0))
    current_light = light_queue[0]


while True:
    read_input()

    print("\nQueue Status:")
    print("AL1:", AL1.size(),
          "BL1:", BL1.size(),
          "CL1:", CL1.size(),
          "DL1:", DL1.size(),
          "AL2 (Priority):", AL2.size())

    # -------- PRIORITY CONDITION --------
    if AL2.size() > 10:
        print("Priority condition active: AL2 served first")
        served = serve_queue(AL2, AL2.size())
        time.sleep(served * TIME_PER_VEHICLE)

    # -------- NORMAL CONDITION --------
    else:
        print(f"Green light on road {current_light}")

        if current_light == "A":
            serve_queue(AL1, 1)
        elif current_light == "B":
            serve_queue(BL1, 1)
        elif current_light == "C":
            serve_queue(CL1, 1)
        elif current_light == "D":
            serve_queue(DL1, 1)

        time.sleep(TIME_PER_VEHICLE)
        next_light()

    time.sleep(1)
