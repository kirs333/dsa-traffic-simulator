from queue import Queue
import time

road_A = Queue()
road_B = Queue()
road_C = Queue()
road_D = Queue()

AL2 = Queue()

def add_vehicle(road):
    if road == "A":
        road_A.enqueue(1)
        AL2.enqueue(1) 
    elif road == "B":
        road_B.enqueue(1)
    elif road == "C":
        road_C.enqueue(1)
    elif road == "D":
        road_D.enqueue(1)

def read_input_file():
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()

        open("input.txt", "w").close()  

        for line in lines:
            add_vehicle(line.strip())

    except FileNotFoundError:
        pass

while True:
    read_input_file()

    print("Queue Status:")
    print("Road A:", road_A.size())
    print("Road B:", road_B.size())
    print("Road C:", road_C.size())
    print("Road D:", road_D.size())
    print("Priority Lane AL2:", AL2.size())
    print("-" * 30)

    time.sleep(2)

