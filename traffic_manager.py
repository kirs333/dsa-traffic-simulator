import random
import os

# ================= CONSTANTS =================
WIDTH = 700
HEIGHT = 500

INTERSECTION = {
    'x1': 280,
    'x2': 420,
    'y1': 185,
    'y2': 315
}

CAR_SPEED = 3
GAP = 40

# Traffic Control Constants
TIME_PER_CAR = 800
MIN_DURATION = 2000
PRIORITY_LANE = "up"
PRIORITY_THRESHOLD = 10
PRIORITY_RELEASE = 5
STARTUP_BUFFER = 3000

# Lane Centers
VERT_LEFT = 303
VERT_MIDDLE = 350
VERT_RIGHT = 397
HORZ_TOP = 208
HORZ_MIDDLE = 255
HORZ_BOTTOM = 302

# Stop Lines
STOP_UP = INTERSECTION['y2'] + 10
STOP_DOWN = INTERSECTION['y1'] - 10
STOP_RIGHT = INTERSECTION['x1'] - 10
STOP_LEFT = INTERSECTION['x2'] + 10

# ================= CAR LOGIC CLASS =================
class CarLogic:
    def __init__(self, car_id, direction, lane_type):
        self.id = car_id
        self.spawn_direction = direction
        self.lane_type = lane_type
        self.current_direction = direction
        self.turned = False
        self.passed = False
        self.in_queue = False
        
        # Generate random color
        colors = ["#FF4444", "#4444FF", "#FFCC00", "#00CC66", "#FF8800", "#CC00CC"]
        self.color = random.choice(colors)
        
        # Initialize position and dimensions based on spawn direction
        if direction == "up":
            self.y = HEIGHT + 40
            if lane_type == "turn":
                self.x = VERT_LEFT
                self.target_lane = HORZ_BOTTOM
            else:
                self.x = VERT_MIDDLE
                self.target_lane = None
            self.w, self.h = 22, 30
            
        elif direction == "down":
            self.y = -40
            if lane_type == "turn":
                self.x = VERT_RIGHT
                self.target_lane = HORZ_TOP
            else:
                self.x = VERT_MIDDLE
                self.target_lane = None
            self.w, self.h = 22, 30
            
        elif direction == "right":
            self.x = -40
            if lane_type == "turn":
                self.y = HORZ_TOP
                self.target_lane = VERT_LEFT
            else:
                self.y = HORZ_MIDDLE
                self.target_lane = None
            self.w, self.h = 30, 22
            
        elif direction == "left":
            self.x = WIDTH + 40
            if lane_type == "turn":
                self.y = HORZ_BOTTOM
                self.target_lane = VERT_RIGHT
            else:
                self.y = HORZ_MIDDLE
                self.target_lane = None
            self.w, self.h = 30, 22
    
    def check_and_execute_turn(self):
        """Handle turning logic"""
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
    
    def move(self):
        """Update car position"""
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
        
        self.x += dx
        self.y += dy
    
    def in_intersection(self):
        """Check if car is inside intersection"""
        buffer = 10
        return (INTERSECTION['x1'] - buffer < self.x < INTERSECTION['x2'] + buffer and 
                INTERSECTION['y1'] - buffer < self.y < INTERSECTION['y2'] + buffer)
    
    def off_screen(self):
        """Check if car has left the visible area"""
        return (self.x < -60 or self.x > WIDTH + 60 or 
                self.y < -60 or self.y > HEIGHT + 60)

# ================= TRAFFIC MANAGER =================
class TrafficManager:
    def __init__(self):
        self.cars = []
        self.car_id_counter = 0
        self.lane_queues = {"up": [], "down": [], "left": [], "right": []}
        self.current_green = "up"
        self.last_switch_time = 0
        self.next_switch_duration = MIN_DURATION
        self.tick_count = 0
        
        # Initialize file reading
        if not os.path.exists("input.txt"):
            with open("input.txt", "w") as f:
                f.write("")
        
        self.file_handle = open("input.txt", "r")
        self.file_handle.seek(0, 2)  # Go to end of file
    
    def read_generator(self):
        """Read new vehicle data from input.txt"""
        lines = self.file_handle.readlines()
        for line in lines:
            line = line.strip()
            if line and ',' in line:
                parts = line.split(',')
                direction = parts[0].strip()
                lane_type = parts[1].strip()
                
                # Create new car
                new_car = CarLogic(self.car_id_counter, direction, lane_type)
                self.cars.append(new_car)
                self.car_id_counter += 1
    
    def get_lane_id(self, car):
        """Get lane identifier for car"""
        if car.current_direction in ["up", "down"]:
            return (car.current_direction, round(car.x / 15) * 15)
        else:
            return (car.current_direction, round(car.y / 15) * 15)
    
    def find_car_ahead(self, car):
        """Find the car directly in front"""
        lane_id = self.get_lane_id(car)
        closest = None
        min_dist = float('inf')
        
        for other in self.cars:
            if other == car or self.get_lane_id(other) != lane_id:
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
    
    def is_intersection_blocked(self, car):
        """Check if intersection is blocked by other straight cars"""
        for other in self.cars:
            if other == car:
                continue
            
            if other.lane_type == "turn":
                continue
            
            if other.in_intersection():
                if other.spawn_direction != car.spawn_direction:
                    return True
        return False
    
    def can_move(self, car, front_car):
        """Determine if car can move forward"""
        if car.passed:
            self.remove_from_queue(car)
            return True
        
        if car.in_intersection():
            self.remove_from_queue(car)
            return True
        
        # Calculate distance to stop line
        dist = 0
        if car.current_direction == "up":
            dist = car.y - STOP_UP
        elif car.current_direction == "down":
            dist = STOP_DOWN - car.y
        elif car.current_direction == "right":
            dist = STOP_RIGHT - car.x
        elif car.current_direction == "left":
            dist = car.x - STOP_LEFT
        
        # Traffic light check (straight cars only)
        if car.lane_type == "straight":
            is_green = (car.current_direction == self.current_green)
            
            if not is_green and 0 <= dist <= GAP:
                self.add_to_queue(car)
                return False
            
            # Intersection clearance check
            if 0 <= dist <= GAP:
                if self.is_intersection_blocked(car):
                    return False
        
        # Front car collision check
        if front_car:
            gap = 0
            if car.current_direction == "up":
                gap = car.y - front_car.y
            elif car.current_direction == "down":
                gap = front_car.y - car.y
            elif car.current_direction == "right":
                gap = front_car.x - car.x
            elif car.current_direction == "left":
                gap = car.x - front_car.x
            
            if 0 < gap < GAP:
                return False
        
        self.remove_from_queue(car)
        return True
    
    def add_to_queue(self, car):
        """Add car to waiting queue"""
        if not car.in_queue and car.lane_type == "straight":
            if car not in self.lane_queues[car.current_direction]:
                self.lane_queues[car.current_direction].append(car)
                car.in_queue = True
    
    def remove_from_queue(self, car):
        """Remove car from waiting queue"""
        if car.in_queue:
            try:
                self.lane_queues[car.current_direction].remove(car)
                car.in_queue = False
            except ValueError:
                pass
    
    def update_traffic_lights(self):
        """Smart traffic light controller"""
        self.tick_count += 1
        
        # Check if it's time to switch
        if self.tick_count * 30 < self.last_switch_time + self.next_switch_duration:
            return
        
        # Time to switch!
        priority_count = len(self.lane_queues[PRIORITY_LANE])
        
        # Priority logic
        if priority_count > PRIORITY_THRESHOLD:
            if self.current_green != PRIORITY_LANE:
                self.current_green = PRIORITY_LANE
                self.next_switch_duration = (priority_count * TIME_PER_CAR) + 2000
                print(f"⚠️ PRIORITY MODE: {priority_count} cars in {PRIORITY_LANE.upper()}")
            else:
                if priority_count < PRIORITY_RELEASE:
                    order = ["up", "left", "down", "right"]
                    idx = order.index(self.current_green)
                    self.current_green = order[(idx + 1) % 4]
                    self.next_switch_duration = MIN_DURATION
                    print(f"✓ Priority cleared, resuming normal cycle")
                else:
                    self.next_switch_duration = TIME_PER_CAR * 3
        else:
            
            order = ["up", "left", "down", "right"]
            idx = order.index(self.current_green)
            self.current_green = order[(idx + 1) % 4]
            
            waiting_cars = len(self.lane_queues[self.current_green])
            needed_time = waiting_cars * TIME_PER_CAR
            
            if waiting_cars > 0:
                self.next_switch_duration = max(MIN_DURATION, needed_time + STARTUP_BUFFER)
            else:
                self.next_switch_duration = MIN_DURATION
        
        self.last_switch_time = self.tick_count * 30
    
    def update(self):
        """Main update loop - called every frame"""
        # Read new cars from generator
        self.read_generator()
        
        # Update traffic lights
        self.update_traffic_lights()
        
        # Move cars
        for car in self.cars[:]:
            front = self.find_car_ahead(car)
            
            if self.can_move(car, front):
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
            
            # Remove off-screen cars
            if car.off_screen():
                self.remove_from_queue(car)
                self.cars.remove(car)
    
    def get_state(self):
        """Return current state for visualizer"""
        return {
            "cars": self.cars,
            "lights": self.current_green,
            "queues": {k: len(v) for k, v in self.lane_queues.items()}
        }
    
    def close(self):
        """Cleanup resources"""
        self.file_handle.close()