import random
import time
import os

# Map roads to directions 
roads_map = {
    "A": "up",
    "B": "down",
    "C": "left",
    "D": "right"
}

# Ensure file is empty at start
with open("input.txt", "w") as f:
    f.write("")

print("=" * 50)
print("TRAFFIC GENERATOR STARTED")
print("=" * 50)
print("Generating vehicles and writing to input.txt...")
print("Press Ctrl+C to stop")
print("=" * 50)

try:
    while True:
        road_key = random.choice(list(roads_map.keys()))
        direction = roads_map[road_key]
        
        # Randomly decide if it's a turning car (30% chance)
        lane_type = "turn" if random.random() < 0.3 else "straight"

        
        with open("input.txt", "a") as f:
            f.write(f"{direction},{lane_type}\n")

        print(f"Generated: Road {road_key} → {direction.upper()} ({lane_type})")
        
        # Randomize spawn time for realistic traffic (0.4 to 1.2 seconds)
        time.sleep(random.uniform(0.4, 1.2))
        
except KeyboardInterrupt:
    print("\n" + "=" * 50)
    print("Generator stopped by user")
    print("=" * 50)