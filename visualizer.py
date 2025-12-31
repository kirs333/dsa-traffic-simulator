import tkinter as tk
from traffic_manager import TrafficManager, WIDTH, HEIGHT, INTERSECTION

# ================= WINDOW SETUP =================
root = tk.Tk()
root.title("Smart Queue-Based Traffic System")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#8B7355")
canvas.pack()

# ================= CONSTANTS =================
ROAD_COLOR = "#4A4A4A"
CENTER_COLOR = "#5A5A5A"

# Initialize Traffic Manager
manager = TrafficManager()

# Dictionary to track visual objects: {car_id: (body_id, indicator_id)}
visual_cars = {}

# Traffic light visual objects
traffic_lights = {}

# ================= DRAW STATIC BACKGROUND =================
def draw_static_background():
    """Draw roads, intersections, and stop lines"""
    # Vertical road
    canvas.create_rectangle(280, 0, 420, HEIGHT, fill=ROAD_COLOR, outline="")
    
    # Horizontal road
    canvas.create_rectangle(0, 185, WIDTH, 315, fill=ROAD_COLOR, outline="")
    
    # Intersection center
    canvas.create_rectangle(
        INTERSECTION['x1'], INTERSECTION['y1'],
        INTERSECTION['x2'], INTERSECTION['y2'],
        fill=CENTER_COLOR, outline=""
    )
    
    # Lane dividers (vertical)
    canvas.create_line(320, 0, 320, HEIGHT, fill="white", width=2, dash=(10, 10))
    canvas.create_line(380, 0, 380, HEIGHT, fill="white", width=2, dash=(10, 10))
    
    # Lane dividers (horizontal)
    canvas.create_line(0, 227, WIDTH, 227, fill="white", width=2, dash=(10, 10))
    canvas.create_line(0, 263, WIDTH, 263, fill="white", width=2, dash=(10, 10))
    
    # Stop lines
    canvas.create_line(280, 325, 420, 325, fill="yellow", width=3)  # UP
    canvas.create_line(280, 175, 420, 175, fill="yellow", width=3)  # DOWN
    canvas.create_line(270, 185, 270, 315, fill="yellow", width=3)  # RIGHT
    canvas.create_line(430, 185, 430, 315, fill="yellow", width=3)  # LEFT

# ================= TRAFFIC LIGHTS =================
def create_traffic_lights():
    """Create traffic light indicators"""
    global traffic_lights
    
    # UP lane light
    light_up = canvas.create_oval(345, 320, 360, 335, fill="red", outline="white", width=2)
    canvas.create_text(352, 345, text="UP", fill="white", font=("Arial", 8, "bold"))
    
    # DOWN lane light
    light_down = canvas.create_oval(365, 175, 380, 190, fill="red", outline="white", width=2)
    canvas.create_text(372, 165, text="DOWN", fill="white", font=("Arial", 8, "bold"))
    
    # LEFT lane light
    light_left = canvas.create_oval(425, 245, 440, 260, fill="red", outline="white", width=2)
    canvas.create_text(450, 252, text="LEFT", fill="white", font=("Arial", 8, "bold"))
    
    # RIGHT lane light
    light_right = canvas.create_oval(260, 265, 275, 280, fill="red", outline="white", width=2)
    canvas.create_text(245, 272, text="RIGHT", fill="white", font=("Arial", 8, "bold"))
    
    traffic_lights = {
        "up": light_up,
        "down": light_down,
        "left": light_left,
        "right": light_right
    }

# Queue display text
queue_text = canvas.create_text(10, 10, anchor="nw", text="", fill="white", 
                                font=("Arial", 10, "bold"))

# ================= UPDATE FUNCTIONS =================
def update_traffic_lights_display(green_direction):
    """Update traffic light colors"""
    for direction, light_id in traffic_lights.items():
        if direction == green_direction:
            canvas.itemconfig(light_id, fill="green")
        else:
            canvas.itemconfig(light_id, fill="red")

def update_queue_display(queues, green_direction):
    """Update queue count display"""
    text = "Queue Counts:\n"
    for direction in ["up", "down", "left", "right"]:
        count = queues.get(direction, 0)
        indicator = " ← GREEN" if direction == green_direction else ""
        priority_mark = " [PRIORITY]" if direction == "up" else ""
        text += f"{direction.upper()}: {count}{priority_mark}{indicator}\n"
    canvas.itemconfig(queue_text, text=text)

def update_visuals():
    """Main visualization update loop"""
    # Get updated state from traffic manager
    manager.update()
    state = manager.get_state()
    
    # Update traffic lights
    green_direction = state['lights']
    update_traffic_lights_display(green_direction)
    
    # Update queue display
    update_queue_display(state['queues'], green_direction)
    
    # Track current car IDs
    current_car_ids = set()
    
    # Update or create cars
    for car_logic in state['cars']:
        current_car_ids.add(car_logic.id)
        
        if car_logic.id not in visual_cars:
            # New car - create visual representation
            body_id = canvas.create_rectangle(
                car_logic.x - car_logic.w/2, car_logic.y - car_logic.h/2,
                car_logic.x + car_logic.w/2, car_logic.y + car_logic.h/2,
                fill=car_logic.color, outline="white", width=1
            )
            
            # Indicator dot
            indicator_color = "orange" if car_logic.lane_type == "turn" else "lightblue"
            indicator_id = canvas.create_oval(
                car_logic.x - 4, car_logic.y - 4,
                car_logic.x + 4, car_logic.y + 4,
                fill=indicator_color, outline=""
            )
            
            visual_cars[car_logic.id] = (body_id, indicator_id)
        else:
            # Existing car - update position
            body_id, indicator_id = visual_cars[car_logic.id]
            
            canvas.coords(
                body_id,
                car_logic.x - car_logic.w/2, car_logic.y - car_logic.h/2,
                car_logic.x + car_logic.w/2, car_logic.y + car_logic.h/2
            )
            
            canvas.coords(
                indicator_id,
                car_logic.x - 4, car_logic.y - 4,
                car_logic.x + 4, car_logic.y + 4
            )
    
    # Remove cars that no longer exist in logic
    for car_id in list(visual_cars.keys()):
        if car_id not in current_car_ids:
            body_id, indicator_id = visual_cars[car_id]
            canvas.delete(body_id)
            canvas.delete(indicator_id)
            del visual_cars[car_id]
    
    # Schedule next update (30ms = ~33 FPS)
    root.after(30, update_visuals)

# ================= CLEANUP =================
def on_closing():
    """Clean up resources when closing"""
    manager.close()
    root.destroy()

# ================= START APPLICATION =================
print("=" * 60)
print("SMART QUEUE-BASED TRAFFIC VISUALIZATION")
print("=" * 60)
print("Architecture:")
print("  → generator.py: Generates vehicle data")
print("  → traffic_manager.py: Handles traffic logic")
print("  → visualizer.py: Displays the simulation")
print("=" * 60)
print("Make sure generator.py is running in another terminal!")
print("=" * 60)

# Set up close handler
root.protocol("WM_DELETE_WINDOW", on_closing)

# Draw static elements
draw_static_background()
create_traffic_lights()

# Start update loop
update_visuals()

# Start Tkinter main loop
root.mainloop()