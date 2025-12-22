import random
import time

roads = ["A", "B", "C", "D"]

while True:
    road = random.choice(roads)

    with open("input.txt", "a") as f:
        f.write(road + "\n")

    print(f"Vehicle generated on road {road}")
    time.sleep(1)

