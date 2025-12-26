import time
from myqueue import Queue

LOG_FILE = "simulation.log"

PRIORITY_ACTIVATION_THRESHOLD = 10
PRIORITY_RELEASE_THRESHOLD = 5
STATS_PRINT_INTERVAL = 5


total_served = 0
served_per_road = {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0,
    "AL2": 0
}
priority_activations = 0
cycle_count = 0

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
GREEN_TIME = 3


def read_input():
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()

        open("input.txt", "w").close()

        for road in lines:
            road = road.strip()
            if road == "A":
                AL2.enqueue("V")
            elif road in road_map:
                road_map[road].enqueue("V")
    except FileNotFoundError:
        pass


def serve(queue, seconds, road_name):
    global total_served, served_per_road

    served = 0
    start = time.time()

    while not queue.is_empty():
        if time.time() - start >= seconds:
            break
        queue.dequeue()
        served += 1
        total_served += 1
        served_per_road[road_name] += 1
        time.sleep(TIME_PER_VEHICLE)

    return served

def log_event(message):
    with open(LOG_FILE, "a") as log:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")


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
    if AL2.size() > PRIORITY_ACTIVATION_THRESHOLD:
     priority_activations += 1
     log_event("Priority lane AL2 activated")
     print("Priority light GREEN for AL2")
     served = serve(AL2, GREEN_TIME, "AL2")
     log_event(f"AL2 served {served} vehicles")
     print("Vehicles passed from AL2:", served)
     continue


    # Normal traffic light rotation
    road = roads[current_road_index]
    queue = road_map[road]

    print(f"GREEN light for Road {road}")
    log_event(f"Green light for Road {road}")

    served = serve(queue, GREEN_TIME, road)
    log_event(f"Road {road} served {served} vehicles")

    print(f"Vehicles passed from Road {road}:", served)

    current_road_index = (current_road_index + 1) % len(roads)
    cycle_count += 1

    if cycle_count % STATS_PRINT_INTERVAL == 0:
      print("\n--- SIMULATION STATS ---")
      print("Total vehicles served:", total_served)
      print("Served per road:", served_per_road)
      print("Priority activations:", priority_activations)
      print("------------------------")

    time.sleep(1)

