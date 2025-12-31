# Smart Queue-Based Traffic System Simulation

**Assignment Number:** Assignment 1

**Course:** Data Structures and Algorithms (CS-I)

**Author:** Krish Ghimire (Roll No. 24)

## Video 

https://github.com/user-attachments/assets/1c4eefe5-f9b2-4291-a403-70852ee8e678

 Introduction

### Background

Traffic congestion is a major urban problem, leading to lost time and increased emissions. Traditional traffic light systems operate on fixed timers (Round-Robin logic), which allocates green light time regardless of whether a lane is full or empty. This inefficiency often leads to "ghost jams" where cars wait at a red light while the cross-street is empty.

### Problem Statement

The goal of this assignment was to simulate a solution to this inefficiency using standard Data Structures. The challenge was to create a system that can "see" the traffic and make decisions, rather than blindly following a clock.

### Objectives

* To implement a visual simulation of a 4-way intersection.
* To utilize **Queues** to track vehicles waiting in each lane.
* To apply an algorithm that dynamically calculates green light duration based on queue length (`O(1)` lookup).
* To implement a **Priority Lane** feature for emergency or high-density traffic flushing.

---

##  System Requirements

To develop and run this simulation, the following hardware and software environments were used:

* **Operating System:** Windows 10/11, MacOS, or Linux
* **Programming Language:** Python 3.x
* **GUI Library:** Tkinter (Standard Python Library)
* **Modules Used:** `random` (for vehicle spawning), `tkinter` (for graphics)
* **IDE/Text Editor:** VS Code / PyCharm / IDLE

---

##  Key Features

* **Visual Simulation:** A GUI representing a 4-way intersection with moving vehicles, stop lines, and dynamic traffic lights.
* **Queue Detection:** The system automatically detects and counts cars waiting at red lights for each lane.
* **Adaptive Timing:** The duration of the green light is calculated mathematically based on the number of cars waiting:
> 


* **Priority Logic:** A specific "Priority Lane" (Up) is monitored. If traffic in this lane exceeds a threshold (10 cars), the system overrides the normal cycle to flush the congestion until it drops below a safe level (5 cars).
* **Collision Avoidance:** Vehicles utilize a proximity detection system to prevent rear-end collisions and stop at red lights.

---

##  Data Structures

The simulation relies primarily on Lists (functioning as Queues) and Dictionaries to manage vehicle data and state.

| Data Structure | Implementation in Code | Purpose |
| --- | --- | --- |
| **List (Dynamic Array)** | `cars = []` | **Global Object Storage:** Stores all active Car objects currently on the canvas. Used to iterate through vehicles for movement updates and collision checks. |
| **Dictionary of Lists** | `lane_queues = {'up': [], ...}` | **Queue Management:** Specific lists mapped to directions. Acts as a waiting queue to count how many cars are stuck at a red light. |
| **Dictionary** | `traffic_lights = {...}` | **State Management:** Maps direction strings (keys) to tkinter canvas objects (values) to allow `O(1)` access when switching lights. |
| **Class / Object** | `class Car:` | **Entity Encapsulation:** Encapsulates properties (`x`, `y`, `speed`, `direction`) and methods (`move`, `stop`) for individual vehicles. |

### Key Functions using Data Structures

* **`spawn_car()`**: Instantiates a new Car object and appends it to the global `cars` list.
* **`Car.add_to_queue()`**: Checks if a car is stopped; if so, appends the car object to the specific list inside the `lane_queues` dictionary.
* **`Car.remove_from_queue()`**: When a car starts moving, it removes the object from the `lane_queues` list.
* **`Car.is_intersection_blocked()`**: Iterates through the global `cars` list to check if any other vehicle is currently occupying the intersection coordinates.
* **`find_car_ahead(car)`**: Iterates through the `cars` list to calculate the distance between the current vehicle and the closest vehicle in front of it (for collision avoidance).
* **`smart_traffic_controller()`**: Accesses `len(lane_queues[direction])` from the dictionary to calculate the required green light duration.

---

##  Algorithms

The traffic control logic uses a hybrid **Round-Robin with Priority Override** algorithm.

### Step 1: Measurement

The system calculates the length () of the queue for the current Priority Lane (Up).

### Step 2: Priority Check

* **IF  (10 cars):**
* Interrupt normal cycle.
* Set Green Light for Priority Lane.
* Maintain Green Light until  (5 cars).


* **ELSE (Normal Condition):**
* Proceed to the next lane in the cycle (Up → Left → Down → Right).



### Step 3: Dynamic Duration Calculation

Instead of a fixed timer, the Green Light duration () is calculated as:

* `TimePerCar`: 800ms
* `StartupBuffer`: 3000ms (to clear previous intersection traffic)

### Step 4: Execution

Update the GUI to reflect signal changes and wait for time  before recursion.

---

##  Time Complexity Analysis

### 1. Traffic Control Decision (`smart_traffic_controller`)

* **Complexity:** 
* **Explanation:** Accessing the length of a list in Python (`len()`) is a constant time operation. The controller performs a fixed number of checks (Priority check + Duration calculation) regardless of how many cars are on the screen.

### 2. Simulation Animation (`animate` loop)

* **Complexity:** 
* **Explanation:** This is the most computationally expensive part.
1. The `animate` function loops through every active car ().
2. Inside this loop, it calls `find_car_ahead()`.
3. `find_car_ahead()` loops through the list of cars () again to find the closest vehicle in the same lane.


* Therefore, for every frame of animation, the complexity is , or .



### 3. Queue Management (`add` / `remove`)

* **Adding:**  (Appending to the end of a list).
* **Removing:**  (Searching for an item in a list and removing it requires shifting elements).

---

##  Conclusion and Future Scope

The **Smart Queue-Based Traffic System** successfully demonstrates how Data Structures and Algorithms can solve real-world optimization problems. By using Lists as queues and Dictionaries for state management, the system efficiently handles vehicle tracking and signal timing. The implementation of the priority logic shows how algorithmic intervention can prevent traffic overflow.

**Future Enhancements:**

* **AI Integration:** Using Machine Learning to predict traffic patterns before they happen.
* **Ambulance Detection:** Adding a specific "Emergency Vehicle" class that triggers an immediate green light from any direction.
* **Multi-Intersection Network:** Connecting multiple simulation windows to observe how traffic flows between different intersections.

---

##  References

1. Python Software Foundation. "tkinter — Python interface to Tcl/Tk." [Python 3.10 Documentation](https://docs.python.org/3/library/tkinter.html).
2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms*. MIT Press.
3. GeeksforGeeks. "Queue Data Structure." [https://www.geeksforgeeks.org/queue-data-structure/](https://www.geeksforgeeks.org/queue-data-structure/)


