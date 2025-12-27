import tkinter as tk
import random

# ================= WINDOW =================
WIDTH = 700
HEIGHT = 500
root = tk.Tk()
root.title("Smart Queue-Based Traffic System")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#8B7355")
canvas.pack()

# ================= CONSTANTS =================
ROAD_COLOR = "#4A4A4A"
CENTER_COLOR = "#5A5A5A"

INTERSECTION = {
    'x1': 280,
    'x2': 420,
    'y1': 185,
    'y2': 315
}

CAR_SPEED = 3
GAP = 40

# Traffic Control Constants
TIME_PER_CAR = 800  # ms required for one car to pass
MIN_DURATION = 2000  # Minimum green light time
PRIORITY_LANE = "up"  # Define which lane has priority
PRIORITY_THRESHOLD = 10  # Trigger priority mode when queue > 10
PRIORITY_RELEASE = 5  # Exit priority mode when queue < 5

# LANE CENTERS
VERT_LEFT = 303
VERT_MIDDLE = 350
VERT_RIGHT = 397
HORZ_TOP = 208
HORZ_MIDDLE = 255
HORZ_BOTTOM = 302

# Stop lines
STOP_UP = INTERSECTION['y2'] + 10
STOP_DOWN = INTERSECTION['y1'] - 10
STOP_RIGHT = INTERSECTION['x1'] - 10
STOP_LEFT = INTERSECTION['x2'] + 10

# ================= QUEUE SYSTEM =================
lane_queues = {
    "up": [],
    "down": [],
    "left": [],
    "right": []
}

current_green_direction = "up"  # Start with UP lane

# ================= DRAW ROADS =================
canvas.create_rectangle(280, 0, 420, HEIGHT, fill=ROAD_COLOR, outline="")
canvas.create_rectangle(0, 185, WIDTH, 315, fill=ROAD_COLOR, outline="")
canvas.create_rectangle(INTERSECTION['x1'], INTERSECTION['y1'], 
                       INTERSECTION['x2'], INTERSECTION['y2'], 
                       fill=CENTER_COLOR, outline="")

# Lane dividers
canvas.create_line(320, 0, 320, HEIGHT, fill="white", width=2, dash=(10, 10))
canvas.create_line(380, 0, 380, HEIGHT, fill="white", width=2, dash=(10, 10))
canvas.create_line(0, 227, WIDTH, 227, fill="white", width=2, dash=(10, 10))
canvas.create_line(0, 263, WIDTH, 263, fill="white", width=2, dash=(10, 10))

# Stop lines
canvas.create_line(280, STOP_UP, 420, STOP_UP, fill="yellow", width=3)
canvas.create_line(280, STOP_DOWN, 420, STOP_DOWN, fill="yellow", width=3)
canvas.create_line(STOP_RIGHT, 185, STOP_RIGHT, 315, fill="yellow", width=3)
canvas.create_line(STOP_LEFT, 185, STOP_LEFT, 315, fill="yellow", width=3)

# ================= TRAFFIC LIGHTS (4 separate lights) =================
# UP lane light (bottom of intersection)
light_up = canvas.create_oval(345, 320, 360, 335, fill="red", outline="white", width=2)
canvas.create_text(352, 345, text="UP", fill="white", font=("Arial", 8, "bold"))

# DOWN lane light (top of intersection)
light_down = canvas.create_oval(365, 175, 380, 190, fill="red", outline="white", width=2)
canvas.create_text(372, 165, text="DOWN", fill="white", font=("Arial", 8, "bold"))

# LEFT lane light (right of intersection)
light_left = canvas.create_oval(425, 245, 440, 260, fill="red", outline="white", width=2)
canvas.create_text(450, 252, text="LEFT", fill="white", font=("Arial", 8, "bold"))

# RIGHT lane light (left of intersection)
light_right = canvas.create_oval(260, 265, 275, 280, fill="red", outline="white", width=2)
canvas.create_text(245, 272, text="RIGHT", fill="white", font=("Arial", 8, "bold"))

traffic_lights = {
    "up": light_up,
    "down": light_down,
    "left": light_left,
    "right": light_right
}

# Queue counter display
queue_text = canvas.create_text(10, 10, anchor="nw", text="", fill="white", 
                                font=("Arial", 10, "bold"))

# ================= SMART TRAFFIC CONTROLLER =================
def update_traffic_lights_graphics(direction):
    """Update visual traffic lights - only one direction is green"""
    for dir_name, light in traffic_lights.items():
        if dir_name == direction:
            canvas.itemconfig(light, fill="green")
        else:
            canvas.itemconfig(light, fill="red")

def update_queue_display():
    """Display queue counts on screen"""
    text = "Queue Counts:\n"
    for direction in ["up", "down", "left", "right"]:
        count = len(lane_queues[direction])
        indicator = " ← GREEN" if direction == current_green_direction else ""
        priority_mark = " [PRIORITY]" if direction == PRIORITY_LANE else ""
        text += f"{direction.upper()}: {count}{priority_mark}{indicator}\n"
    canvas.itemconfig(queue_text, text=text)

def smart_traffic_controller():
    global current_green_direction
    
    # Measure queues
    priority_count = len(lane_queues[PRIORITY_LANE])
    
    next_direction = ""
    duration = 0
    
    # PRIORITY LOGIC CHECK
    if priority_count > PRIORITY_THRESHOLD:
        if current_green_direction != PRIORITY_LANE:
            # Switch immediately to Priority Lane
            next_direction = PRIORITY_LANE
            # Add buffer time for priority lane too
            duration = (priority_count * TIME_PER_CAR) + 2000
            print(f"⚠️ PRIORITY MODE ACTIVATED: {priority_count} cars in {PRIORITY_LANE.upper()}")
        else:
            # Already serving priority lane
            if priority_count < PRIORITY_RELEASE:
                # Priority satisfied, resume normal cycle
                print(f"✓ Priority cleared ({priority_count} < {PRIORITY_RELEASE}), resuming normal cycle")
                order = ["up", "left", "down", "right"]
                current_index = order.index(current_green_direction)
                next_direction = order[(current_index + 1) % 4]
                duration = MIN_DURATION
            else:
                # Still high traffic, keep priority lane green
                next_direction = PRIORITY_LANE
                duration = TIME_PER_CAR * 3  # Short extension
                print(f"⚠️ Priority lane extended: {priority_count} cars remaining")
    
    # NORMAL CONDITION (Round Robin)
    else:
        # Cycle: up -> left -> down -> right -> up...
        order = ["up", "left", "down", "right"]
        current_index = order.index(current_green_direction)
        next_direction = order[(current_index + 1) % 4]
        
        # Calculate duration based on queue length
        waiting_cars = len(lane_queues[next_direction])
        
        # === FIXED TIMING LOGIC ===
        
        # 1. Base time needed for cars to pass
        needed_time = waiting_cars * TIME_PER_CAR
        
        # 2. INCREASED STARTUP BUFFER (Fix for "Wasted Green Light")
        # Increased from 1500 to 3000. 
        # This gives 3 full seconds for the previous cycle's cars to clear out
        # BEFORE we start counting the time against the current queue.
        STARTUP_BUFFER = 3000 
        
        # 3. Ensure duration is NEVER shorter than MIN_DURATION (2000ms)
        if waiting_cars > 0:
            duration = max(MIN_DURATION, needed_time + STARTUP_BUFFER)
        else:
            duration = MIN_DURATION
            
        # === FIX ENDS HERE ===
        
        print(f"Normal cycle: {next_direction.upper()} ({waiting_cars} cars) - {duration}ms")
    
    # Execute switch
    current_green_direction = next_direction
    update_traffic_lights_graphics(next_direction)
    update_queue_display()
    
    # Schedule next check
    root.after(int(duration), smart_traffic_controller)

# ================= CAR CLASS =================
class Car:
    def __init__(self, spawn_direction, lane_type):
        self.spawn_direction = spawn_direction
        self.lane_type = lane_type
        self.current_direction = spawn_direction
        self.turned = False
        self.passed = False
        self.in_queue = False  # Track if car is in queue
        
        colors = ["#FF4444", "#4444FF", "#FFCC00", "#00CC66", "#FF8800", "#CC00CC"]
        self.color = random.choice(colors)
        
        # Spawn logic (same as before)
        if spawn_direction == "up":
            self.y = HEIGHT + 40
            if lane_type == "turn":
                self.x = VERT_LEFT
                self.target_lane = HORZ_BOTTOM
            else:
                self.x = VERT_MIDDLE
                self.target_lane = None
            self.w, self.h = 22, 30
            
        elif spawn_direction == "down":
            self.y = -40
            if lane_type == "turn":
                self.x = VERT_RIGHT
                self.target_lane = HORZ_TOP
            else:
                self.x = VERT_MIDDLE
                self.target_lane = None
            self.w, self.h = 22, 30
            
        elif spawn_direction == "right":
            self.x = -40
            if lane_type == "turn":
                self.y = HORZ_TOP
                self.target_lane = VERT_LEFT
            else:
                self.y = HORZ_MIDDLE
                self.target_lane = None
            self.w, self.h = 30, 22
            
        elif spawn_direction == "left":
            self.x = WIDTH + 40
            if lane_type == "turn":
                self.y = HORZ_BOTTOM
                self.target_lane = VERT_RIGHT
            else:
                self.y = HORZ_MIDDLE
                self.target_lane = None
            self.w, self.h = 30, 22
        
        # Draw car
        self.body = canvas.create_rectangle(
            self.x - self.w/2, self.y - self.h/2,
            self.x + self.w/2, self.y + self.h/2,
            fill=self.color, outline="white", width=1
        )
        
        # Indicator dot
        indicator_color = "orange" if lane_type == "turn" else "lightblue"
        self.indicator = canvas.create_oval(
            self.x - 4, self.y - 4, self.x + 4, self.y + 4,
            fill=indicator_color, outline=""
        )
    
    def check_and_execute_turn(self):
        if self.lane_type != "turn" or self.turned:
            return
        
        turned = False
        
        if self.spawn_direction == "up":
            if self.y <= self.target_lane:
                self.y = self.target_lane
                self.current_direction = "left"
                turned = True
                
        elif self.spawn_direction == "down":
            if self.y >= self.target_lane:
                self.y = self.target_lane
                self.current_direction = "right"
                turned = True
                
        elif self.spawn_direction == "right":
            if self.x >= self.target_lane:
                self.x = self.target_lane
                self.current_direction = "up"
                turned = True
                
        elif self.spawn_direction == "left":
            if self.x <= self.target_lane:
                self.x = self.target_lane
                self.current_direction = "down"
                turned = True
        
        if turned:
            self.turned = True
            self.w, self.h = self.h, self.w
            canvas.coords(self.body,
                          self.x - self.w/2, self.y - self.h/2,
                          self.x + self.w/2, self.y + self.h/2)
            canvas.coords(self.indicator,
                          self.x - 4, self.y - 4,
                          self.x + 4, self.y + 4)
    
    def move(self):
        self.check_and_execute_turn()
        
        dx, dy = 0, 0
        if self.current_direction == "up":
            dy = -CAR_SPEED
        elif self.current_direction == "down":
            dy = CAR_SPEED
        elif self.current_direction == "left":
            dx = -CAR_SPEED
        elif self.current_direction == "right":
            dx = CAR_SPEED
        
        canvas.move(self.body, dx, dy)
        canvas.move(self.indicator, dx, dy)
        self.x += dx
        self.y += dy
    
    def in_intersection(self):
        # Reduced the buffer from 30 to 10.
        # This means a car has to be deeper inside the intersection to count as "in it".
        # This prevents cars waiting at the stop line from triggering the "blocked" flag.
        buffer = 10
        return (INTERSECTION['x1'] - buffer < self.x < INTERSECTION['x2'] + buffer and 
                INTERSECTION['y1'] - buffer < self.y < INTERSECTION['y2'] + buffer)
    
    def is_intersection_blocked(self):
        """Check if the intersection is blocked by STRAIGHT cars from OTHER directions"""
        for other in cars:
            if other == self: 
                continue
            
            # CRITICAL FIX: Ignore turning cars completely.
            # In this simulation, turning cars stay in outer lanes and 
            # physically cannot block the center box.
            if other.lane_type == "turn":
                continue

            # If a STRAIGHT car is physically inside the intersection
            if other.in_intersection():
                # AND that car came from a DIFFERENT direction
                if other.spawn_direction != self.spawn_direction:
                    return True
        return False
    
    def can_move(self, front_car):
        """Check if car can move (Lights + Clearance + Collision)"""
        # 1. If we have already passed the intersection, just drive
        if self.passed:
            self.remove_from_queue()
            return True
        
        # 2. If we are currently INSIDE the intersection, keep moving (don't stop in middle)
        if self.in_intersection():
            self.remove_from_queue()
            return True
        
        # Calculate distance to stop line
        dist = 0
        if self.current_direction == "up":
            dist = self.y - STOP_UP
        elif self.current_direction == "down":
            dist = STOP_DOWN - self.y
        elif self.current_direction == "right":
            dist = STOP_RIGHT - self.x
        elif self.current_direction == "left":
            dist = self.x - STOP_LEFT
        
        # 3. Traffic Light Check (STOP at RED)
        # Only applies to STRAIGHT cars
        if self.lane_type == "straight":
            is_green = (self.current_direction == current_green_direction)
            
            # If Red Light AND we are approaching stop line
            if not is_green and 0 <= dist <= GAP:
                self.add_to_queue()
                return False
        
            # 4. INTERSECTION CLEARANCE CHECK (The Fix for Gridlock)
            # === TURNING CARS BYPASS THIS CHECK ===
            # We ONLY check if the intersection is blocked if we are going STRAIGHT.
            # Turning cars stay on the edge, so they ignore the center blockage.
            if 0 <= dist <= GAP:  
                if self.is_intersection_blocked():
                    return False
            # ======================================

        # 5. Front Car Collision Check (Don't hit the guy ahead of you)
        # This still applies to everyone (even turning cars shouldn't rear-end people)
        if front_car:
            gap = 0
            if self.current_direction == "up":
                gap = self.y - front_car.y
            elif self.current_direction == "down":
                gap = front_car.y - self.y
            elif self.current_direction == "right":
                gap = front_car.x - self.x
            elif self.current_direction == "left":
                gap = self.x - front_car.x
            
            if 0 < gap < GAP:
                return False
        
        # If we passed all checks, we can move!
        self.remove_from_queue()
        return True
    
    def add_to_queue(self):
        """Add car to waiting queue if not already in it"""
        if not self.in_queue and self.lane_type == "straight":
            if self not in lane_queues[self.current_direction]:
                lane_queues[self.current_direction].append(self)
                self.in_queue = True
    
    def remove_from_queue(self):
        """Remove car from waiting queue"""
        if self.in_queue:
            try:
                lane_queues[self.current_direction].remove(self)
                self.in_queue = False
            except ValueError:
                pass  # Car already removed
    
    def off_screen(self):
        return (self.x < -60 or self.x > WIDTH + 60 or 
                self.y < -60 or self.y > HEIGHT + 60)
    
    def destroy(self):
        self.remove_from_queue()  # Clean up queue when car is destroyed
        canvas.delete(self.body)
        canvas.delete(self.indicator)

# ================= STORAGE =================
cars = []

# ================= HELPER FUNCTIONS =================
def get_lane_id(car):
    if car.current_direction in ["up", "down"]:
        return (car.current_direction, round(car.x / 15) * 15)
    else:
        return (car.current_direction, round(car.y / 15) * 15)

def find_car_ahead(car):
    lane_id = get_lane_id(car)
    closest = None
    min_dist = float('inf')
    
    for other in cars:
        if other == car or get_lane_id(other) != lane_id:
            continue
        
        dist = 0
        if car.current_direction == "up":
            dist = car.y - other.y
        elif car.current_direction == "down":
            dist = other.y - car.y
        elif car.current_direction == "right":
            dist = other.x - car.x
        elif car.current_direction == "left":
            dist = car.x - other.x
        
        if 0 < dist < min_dist:
            min_dist = dist
            closest = other
    
    return closest

# ================= SPAWN & ANIMATE =================
def spawn_car():
    # 70% chance to spawn UP cars to test priority queue faster
    if random.randint(0, 10) < 7:
        direction = "up"
    else:
        direction = random.choice(["down", "left", "right"])
    
    lane_type = random.choice(["straight", "turn"])
    
    car = Car(direction, lane_type)
    cars.append(car)
    
    # Heavy traffic: spawn every 0.4-0.8 seconds to build up queues
    root.after(random.randint(400, 800), spawn_car)

def animate():
    for car in cars[:]:
        front = find_car_ahead(car)
        
        if car.can_move(front):
            car.move()
            
            # Mark as passed
            if car.current_direction == "up" and car.y < INTERSECTION['y1'] - 30:
                car.passed = True
            elif car.current_direction == "down" and car.y > INTERSECTION['y2'] + 30:
                car.passed = True
            elif car.current_direction == "right" and car.x > INTERSECTION['x2'] + 30:
                car.passed = True
            elif car.current_direction == "left" and car.x < INTERSECTION['x1'] - 30:
                car.passed = True
        
        if car.off_screen():
            car.destroy()
            cars.remove(car)
    
    # Update queue display periodically
    update_queue_display()
    
    root.after(30, animate)

# ================= START =================
print("=" * 50)
print("SMART QUEUE-BASED TRAFFIC SYSTEM")
print("=" * 50)
print(f"Priority Lane: {PRIORITY_LANE.upper()}")
print(f"Priority activates when queue > {PRIORITY_THRESHOLD}")
print(f"Priority releases when queue < {PRIORITY_RELEASE}")
print("=" * 50)

spawn_car()
animate()
smart_traffic_controller()
root.mainloop()