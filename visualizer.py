import tkinter as tk
import random

# ---------------- WINDOW ----------------
WIDTH = 600
HEIGHT = 400

root = tk.Tk()
root.title("Traffic Simulation")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# ---------------- ROADS ----------------
# Vertical road
canvas.create_rectangle(250, 0, 350, HEIGHT, fill="#dddddd", outline="")
# Horizontal road
canvas.create_rectangle(0, 150, WIDTH, 250, fill="#dddddd", outline="")
# Center box
canvas.create_rectangle(250, 150, 350, 250, fill="#bbbbbb", outline="")

# ---------------- LANES ----------------
LANES_VERTICAL = [270, 300, 330]
LANE_WIDTH = 30

STOP_LINE_Y = 250  # before intersection
CENTER_Y = 200

# Draw lane markings
for x in LANES_VERTICAL:
    canvas.create_line(x - LANE_WIDTH // 2, 0, x - LANE_WIDTH // 2, HEIGHT, dash=(4, 4))
    canvas.create_line(x + LANE_WIDTH // 2, 0, x + LANE_WIDTH // 2, HEIGHT, dash=(4, 4))

# ---------------- TRAFFIC LIGHTS ----------------
light_vertical = canvas.create_oval(360, 170, 380, 190, fill="green")
light_horizontal = canvas.create_oval(170, 360, 190, 380, fill="red")

current_green = "vertical"

def switch_lights():
    global current_green
    if current_green == "vertical":
        current_green = "horizontal"
        canvas.itemconfig(light_vertical, fill="red")
        canvas.itemconfig(light_horizontal, fill="green")
    else:
        current_green = "vertical"
        canvas.itemconfig(light_vertical, fill="green")
        canvas.itemconfig(light_horizontal, fill="red")

    root.after(4000, switch_lights)

# ---------------- CAR CLASS ----------------
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.in_intersection = False

        color = random.choice(["red", "blue", "green", "purple"])

        self.body = canvas.create_rectangle(
            x - 15, y - 10, x + 15, y + 10, fill=color
        )
        self.w1 = canvas.create_oval(x - 12, y + 6, x - 4, y + 14, fill="black")
        self.w2 = canvas.create_oval(x + 4, y + 6, x + 12, y + 14, fill="black")

    def move(self, dy):
        canvas.move(self.body, 0, dy)
        canvas.move(self.w1, 0, dy)
        canvas.move(self.w2, 0, dy)
        self.y += dy

    def destroy(self):
        canvas.delete(self.body)
        canvas.delete(self.w1)
        canvas.delete(self.w2)

# ---------------- CAR STORAGE ----------------
cars_vertical = {lane: [] for lane in LANES_VERTICAL}

# ---------------- SPAWN ----------------
def spawn_car():
    lane = random.choice(LANES_VERTICAL)
    car = Car(lane, HEIGHT + 40)
    cars_vertical[lane].append(car)
    root.after(1500, spawn_car)

# ---------------- ANIMATION ----------------
def animate():
    for lane, lane_cars in cars_vertical.items():
        for i, car in enumerate(lane_cars):

            # spacing between cars
            if i > 0:
                front = lane_cars[i - 1]
                if car.y - front.y < 35:
                    continue

            # enter intersection
            if car.y <= CENTER_Y:
                car.in_intersection = True

            # movement logic
            if car.in_intersection:
                car.move(-4)
            elif current_green == "vertical" or car.y > STOP_LINE_Y:
                car.move(-4)

            # remove car
            if car.y < -50:
                car.destroy()
                lane_cars.remove(car)

    root.after(40, animate)

# ---------------- START ----------------
spawn_car()
animate()
switch_lights()

root.mainloop()
