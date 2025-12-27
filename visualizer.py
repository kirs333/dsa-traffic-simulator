import tkinter as tk
import random

# ================= WINDOW =================
WIDTH = 700
HEIGHT = 500
root = tk.Tk()
root.title("Traffic Junction Simulation")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# ================= CONSTANTS =================
ROAD_COLOR = "#dddddd"
CENTER_COLOR = "#bbbbbb"

# Vertical lanes (top to bottom traffic) - much wider spacing
VERT_LANES = [310, 350, 390]  # leftmost (310) is priority lane AL2

# Horizontal lanes (left to right traffic) - much wider spacing, evenly distributed
HORZ_LANES = [215, 250, 285]

# Intersection boundaries - made much wider
INTERSECTION = {
    'x1': 280,
    'x2': 420,
    'y1': 185,
    'y2': 315
}

# Stop lines (where cars should stop at red lights)
VERT_STOP_LINE = INTERSECTION['y2'] + 15  # Bottom of intersection + buffer
HORZ_STOP_LINE = INTERSECTION['x1'] - 15  # Left of intersection - buffer

CAR_SPEED = 3
GAP = 30  # Further reduced gap

# ================= DRAW ROADS =================
# Vertical road - much wider
canvas.create_rectangle(280, 0, 420, HEIGHT, fill=ROAD_COLOR, outline="")
# Horizontal road - much wider
canvas.create_rectangle(0, 185, WIDTH, 315, fill=ROAD_COLOR, outline="")
# Intersection
canvas.create_rectangle(
    INTERSECTION['x1'], INTERSECTION['y1'], 
    INTERSECTION['x2'], INTERSECTION['y2'], 
    fill=CENTER_COLOR, outline=""
)

# Lane markings for vertical road - solid black lines, evenly spaced
canvas.create_line(330, 0, 330, HEIGHT, fill="black", width=2)  # Between lane 1 and 2
canvas.create_line(370, 0, 370, HEIGHT, fill="black", width=2)  # Between lane 2 and 3

# Lane markings for horizontal road - solid black lines, evenly spaced
canvas.create_line(0, 232, WIDTH, 232, fill="black", width=2)  # Between lane 1 and 2
canvas.create_line(0, 267, WIDTH, 267, fill="black", width=2)  # Between lane 2 and 3

# Stop lines
canvas.create_line(280, VERT_STOP_LINE, 420, VERT_STOP_LINE, fill="white", width=3)
canvas.create_line(HORZ_STOP_LINE, 185, HORZ_STOP_LINE, 315, fill="white", width=3)

# ================= TRAFFIC LIGHTS =================
# Vertical traffic lights (below intersection, for vertical traffic)
light_v_red = canvas.create_oval(340, 305, 355, 320, fill="red")
light_v_green = canvas.create_oval(360, 305, 375, 320, fill="gray")

# Horizontal traffic lights (left of intersection, for horizontal traffic)
light_h_red = canvas.create_oval(280, 225, 295, 240, fill="gray")
light_h_green = canvas.create_oval(280, 245, 295, 260, fill="green")

current_green = "horizontal"

# ================= HELPER FUNCTIONS =================
def intersection_clear():
    """Check if any car is currently in the intersection"""
    for lane in cars_vertical.values():
        for car in lane:
            if car.in_intersection():
                return False
    for lane in cars_horizontal.values():
        for car in lane:
            if car.in_intersection():
                return False
    return True

def switch_lights():
    """Switch traffic lights between horizontal and vertical"""
    global current_green
    
    if not intersection_clear():
        root.after(500, switch_lights)
        return

    if current_green == "horizontal":
        current_green = "vertical"
        canvas.itemconfig(light_v_red, fill="gray")
        canvas.itemconfig(light_v_green, fill="green")
        canvas.itemconfig(light_h_red, fill="red")
        canvas.itemconfig(light_h_green, fill="gray")
    else:
        current_green = "horizontal"
        canvas.itemconfig(light_v_red, fill="red")
        canvas.itemconfig(light_v_green, fill="gray")
        canvas.itemconfig(light_h_red, fill="gray")
        canvas.itemconfig(light_h_green, fill="green")

    root.after(3000, switch_lights)  # Faster light changes (3 seconds instead of 5)

# ================= CAR CLASS =================
class Car:
    def __init__(self, x, y, direction, lane, priority=False):
        self.x = x
        self.y = y
        self.dir = direction
        self.lane = lane
        self.priority = priority
        self.turned = False
        self.passed_intersection = False
        self.turn_target_y = HORZ_LANES[2]  # Bottom horizontal lane (285) for turning cars

        color = random.choice(
            ["red", "blue", "green", "orange", "purple", "cyan", "yellow"]
        )

        if direction == "vertical":
            self.body = canvas.create_rectangle(
                x - 14, y - 10, x + 14, y + 10, fill=color
            )
            self.w1 = canvas.create_oval(x - 12, y - 8, x - 4, y, fill="black")
            self.w2 = canvas.create_oval(x + 4, y - 8, x + 12, y, fill="black")
        else:  # horizontal
            self.body = canvas.create_rectangle(
                x - 10, y - 14, x + 10, y + 14, fill=color
            )
            self.w1 = canvas.create_oval(x - 8, y - 12, x, y - 4, fill="black")
            self.w2 = canvas.create_oval(x - 8, y + 4, x, y + 12, fill="black")

    def move(self, dx, dy):
        canvas.move(self.body, dx, dy)
        canvas.move(self.w1, dx, dy)
        canvas.move(self.w2, dx, dy)
        self.x += dx
        self.y += dy

    def in_intersection(self):
        """Check if car is currently inside the intersection"""
        return (INTERSECTION['x1'] < self.x < INTERSECTION['x2'] and 
                INTERSECTION['y1'] < self.y < INTERSECTION['y2'])

    def can_move_vertical(self, front_car):
        """Determine if vertical car can move forward"""
        # 1. If we have already passed or are inside, keep moving
        if self.passed_intersection or self.in_intersection():
            return True
        
        dist_to_stop_line = self.y - VERT_STOP_LINE

        # 2. Priority Lane Logic (ignores traffic lights)
        if self.priority:
            pass # Priority cars ignore lights and intersection checks
            
        # 3. Normal Lanes Logic
        else:
            # Condition A: Stop if the light is Red
            if current_green != "vertical" and 0 <= dist_to_stop_line <= GAP:
                return False
            
            # Condition B: CRASH PREVENTION - Check if HORIZONTAL cars are blocking
            # Even if the light is Green, we must wait if a HORIZONTAL car is still inside
            horizontal_is_in_way = False
            for lane in cars_horizontal.values():
                for h_car in lane:
                    if h_car.in_intersection():
                        horizontal_is_in_way = True
                        break
                if horizontal_is_in_way:
                    break
            
            # If horizontal traffic is blocking us, wait at the line
            if horizontal_is_in_way and 0 <= dist_to_stop_line <= GAP:
                return False

        # 4. Gap Check (Prevent rear-ending the car in front)
        if front_car and not front_car.turned:
            # Vertical cars move UP (y decreases), so Self.y > Front.y
            gap = self.y - front_car.y
            if 0 < gap < GAP:
                return False
        
        return True

    def can_move_horizontal(self, front_car):
        """Determine if horizontal car can move forward"""
        # 1. If we have already passed or are inside, keep moving
        if self.passed_intersection or self.in_intersection():
            return True
        
        dist_to_stop_line = HORZ_STOP_LINE - self.x
        
        # 2. Stop if the light is Red AND we are close to the stop line
        if current_green != "horizontal" and 0 <= dist_to_stop_line <= GAP:
            return False
        
        # 3. CRASH PREVENTION - Check if VERTICAL cars are blocking
        # Even if the light is Green, wait if a VERTICAL car is still inside
        vertical_is_in_way = False
        for lane in cars_vertical.values():
            for v_car in lane:
                if v_car.in_intersection():
                    vertical_is_in_way = True
                    break
            if vertical_is_in_way:
                break
        
        # If vertical traffic is blocking us, wait at the line
        if vertical_is_in_way and 0 <= dist_to_stop_line <= GAP:
            return False
        
        # 4. Gap Check (Prevent rear-ending)
        if front_car:
            # Horizontal cars move RIGHT, so front_car.x is LARGER than self.x
            gap = front_car.x - self.x
            # Stop if the car in front is too close
            if 0 < gap < GAP + 25:  # Added buffer for car size
                return False
        
        return True

    def destroy(self):
        canvas.delete(self.body)
        canvas.delete(self.w1)
        canvas.delete(self.w2)

# ================= STORAGE =================
cars_vertical = {x: [] for x in VERT_LANES}
cars_horizontal = {y: [] for y in HORZ_LANES}

# ================= SPAWN FUNCTIONS =================
def spawn_vertical():
    lane = random.choice(VERT_LANES)
    priority = (lane == VERT_LANES[0])  # Leftmost lane is priority
    car = Car(lane, HEIGHT + 40, "vertical", lane, priority)
    cars_vertical[lane].append(car)
    root.after(random.randint(1800, 2500), spawn_vertical)  # Reduced spawn rate

def spawn_horizontal():
    # Only spawn in top two lanes (not the bottommost lane at 285)
    lane = random.choice([HORZ_LANES[0], HORZ_LANES[1]])  # Only lanes 215 and 250
    car = Car(-40, lane, "horizontal", lane)
    cars_horizontal[lane].append(car)
    root.after(random.randint(2200, 3000), spawn_horizontal)  # Reduced spawn rate

# ================= ANIMATION LOOP =================
def animate():
    # Animate vertical cars (moving upward)
    for lane, lane_cars in cars_vertical.items():
        for i, car in enumerate(lane_cars):
            front_car = lane_cars[i - 1] if i > 0 else None
            
            # Priority lane turns left
            if car.priority:
                # Start turning when reaching the bottom horizontal lane level
                if not car.turned and car.y <= car.turn_target_y:
                    car.dir = "horizontal"
                    car.turned = True
                    car.y = car.turn_target_y  # Snap to the bottom lane immediately
                
                if car.turned:
                    # Move left on the bottom lane
                    car.move(-CAR_SPEED, 0)
                    if car.x < INTERSECTION['x1']:
                        car.passed_intersection = True
                else:
                    # Moving up before turn - stop at the bottom horizontal lane level
                    if car.can_move_vertical(front_car) and car.y > car.turn_target_y:
                        car.move(0, -CAR_SPEED)
                    elif car.y <= car.turn_target_y:
                        # Ready to turn
                        car.turned = True
                        car.dir = "horizontal"
                        car.y = car.turn_target_y
            else:
                # Normal lanes go straight
                if car.can_move_vertical(front_car):
                    car.move(0, -CAR_SPEED)
                    # Mark as passed once beyond intersection
                    if car.y < INTERSECTION['y1']:
                        car.passed_intersection = True
            
            # Remove cars that left the screen
            if car.y < -60 or car.x < -60:
                car.destroy()
                lane_cars.remove(car)

    # Animate horizontal cars (moving right)
    for lane, lane_cars in cars_horizontal.items():
        for i, car in enumerate(lane_cars):
            front_car = lane_cars[i - 1] if i > 0 else None
            
            if car.can_move_horizontal(front_car):
                car.move(CAR_SPEED, 0)
                # Mark as passed once beyond intersection
                if car.x > INTERSECTION['x2']:
                    car.passed_intersection = True
            
            # Remove cars that left the screen
            if car.x > WIDTH + 60:
                car.destroy()
                lane_cars.remove(car)

    root.after(40, animate)

# ================= START SIMULATION =================
spawn_vertical()
spawn_horizontal()
animate()
switch_lights()

root.mainloop()