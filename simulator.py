import time
from myqueue import Queue

LOG_FILE = "simulation.log"
HISTORY_FILE = "history.txt"

PRIORITY_ACTIVATION_THRESHOLD = 10
PRIORITY_RELEASE_THRESHOLD = 5
STATS_PRINT_INTERVAL = 5
light_queue = Queue()

cycle_history = []


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

def record_cycle(road, served, priority_used):
    entry = {
        "time": time.strftime("%H:%M:%S"),
        "road": road,
        "served": served,
        "priority": priority_used
    }
    cycle_history.append(entry)
for road in roads:
  light_queue.enqueue(road)

def get_next_road():
    road = light_queue.dequeue()
    light_queue.enqueue(road)
    return road

def export_history():
    with open(HISTORY_FILE, "w") as f:
        f.write("Time,Road,Served,Priority\n")
        for entry in cycle_history:
            line = f"{entry['time']},{entry['road']},{entry['served']},{entry['priority']}\n"
            f.write(line)

try:
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
            record_cycle("AL2", served, True)
            print("Vehicles passed from AL2:", served)
            light_queue.enqueue("A")

            continue


        # Normal traffic light rotation
        road = get_next_road()
        queue = road_map[road]

        print(f"GREEN light for Road {road}")
        log_event(f"Green light for Road {road}")

        served = serve(queue, GREEN_TIME, road)
        log_event(f"Road {road} served {served} vehicles")

        record_cycle(road, served, False) 

        print(f"Vehicles passed from Road {road}:", served)

        current_road_index = (current_road_index + 1) % len(roads)
        cycle_count += 1

        if cycle_count % STATS_PRINT_INTERVAL == 0:
            print("\n--- SIMULATION STATS ---")
            print("Total vehicles served:", total_served)
            print("Served per road:", served_per_road)
            print("Priority activations:", priority_activations)
            print("Recent cycles:")
            for entry in cycle_history[-5:]:
                print(entry)
                export_history()

            print("------------------------")
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n\nSimulation stopped by user.")
    print("Final Statistics:")
    print("Total vehicles served:", total_served)
    print("Served per road:", served_per_road)
    print("Priority activations:", priority_activations)

    export_history()
    log_event("Simulation stopped manually")

    print("History exported. Exiting safely.")

except KeyboardInterrupt:
    print("\nSimulation stopped.")
    export_history()

