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

roads = ["A", "B", "C", "D"]
current_road_index = 0

TIME_PER_VEHICLE = 1
GREEN_TIME = 3   # seconds per road


def read_input():
    """Read vehicle arrivals from input.txt"""
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()

        open("input.txt", "w").close()

        for road in lines:
            road = road.strip()
            if road == "A":
                AL2.enqueue("V")   # A has priority lane
            elif road in road_map:
                road_map[road].enqueue("V")
    except FileNotFoundError:
        pass


def serve(queue, seconds):
    """Serve vehicles based on green light duration"""
    served = 0
    start = time.time()

    while not queue.is_empty():
        if time.time() - start >= seconds:
            break
        queue.dequeue()
        served += 1
        time.sleep(TIME_PER_VEHICLE)

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

    # Priority interrupt
    if AL2.size() > 10:
        print("Priority light GREEN for AL2")
        served = serve(AL2, GREEN_TIME)
        print("Vehicles passed from AL2:", served)
        continue

    # Normal traffic light rotation
    road = roads[current_road_index]
    queue = road_map[road]

    print(f"GREEN light for Road {road}")
    served = serve(queue, GREEN_TIME)
    print(f"Vehicles passed from Road {road}:", served)

    current_road_index = (current_road_index + 1) % len(roads)

    time.sleep(1)
