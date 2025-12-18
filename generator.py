import random
import time

roads = ["A", "B", "C", "D"]

while True:
    road = random.choice(roads)
    print(f"Vehicle arrived on road {road}")

    # write to file
    with open("input.txt", "a") as f:
        f.write(road + "\n")

    time.sleep(1)
