import tkinter as tk
import random

# ---------------- WINDOW ----------------
WIDTH = 700
HEIGHT = 500

root = tk.Tk()
root.title("Traffic Junction Simulation")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# ---------------- ROADS ----------------
# Vertical
canvas.create_rectangle(310, 0, 390, HEIGHT, fill="#dddddd", outline="")
# Horizontal
canvas.create_rectangle(0, 210, WIDTH, 290, fill="#dddddd", outline="")
# Center
canvas.create_rectangle(310, 210, 390, 290, fill="#bbbbbb", outline="")

# ---------------- LANES ----------------
LANES_VERTICAL = [325, 350, 375]        # leftmost = free left turn
LANES_HORIZONTAL = [225, 250, 275]

STOP_LINE_Y = 290
STOP_LINE_X = 310
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Draw lane markers
for x in LANES_VERTICAL:
    canvas.create_line(x - 15, 0, x - 15, HEIGHT, dash=(4, 4))
    canvas.create_line(x + 15, 0, x + 15, HEIGHT, dash=(4, 4))

for y in LANES_HORIZONTAL:
    canvas.create_line(0, y - 15, WIDTH, y - 15, dash=(4, 4))
    canvas.create_line(0, y + 15, WIDTH, y + 15, dash=(4, 4))

# ---------------- TRAFFIC LIGHTS ----------------
# Vertical lights
light_v_red = canvas.create_rectangle(405, 230, 420, 245, fill="red")
light_v_green = canvas.create_rectangle(405, 250, 420, 265, fill="gray")

# Horizontal lights
light_h_red = canvas.create_rectangle(280, 305, 295, 320, fill="gray")
light_h_green = canvas.create_rectangle(260, 305, 275, 320, fill="green")

current_green = "vertical"

def switch_lights():
    global current_green
    if current_green == "vertical":
        current_green = "horizontal"
        canvas.itemconfig(light_v_red, fill="gray")
        canvas.itemconfig(light_v_green, fill="green")
        canvas.itemconfig(light_h_red, fill="red")
        canvas.itemconfig(light_h_green, fill="gray")
    else:
        current_green = "vertical"
        canvas.itemconfig(light_v_red, fill="red")
        canvas.itemconfig(light_v_green, fill="gray")
        canvas.itemconfig(light_h_red, fill="gray")
        canvas.itemconfig(light_h_green, fill="green")

    root.after(4000, switch_lights)

# ---------------- CAR CLASS ----------------
class Car:
    def __init__(self, x, y, direction, free_turn=False):
        self.x = x
        self.y = y
        self.direction = direction
        self.free_turn = free_turn
        self.turned = False

        color = random.choice(
            ["red", "blue", "green", "purple", "orange", "cyan", "pink"]
        )

        self.body = canvas.create_rectangle(
            x - 14, y - 10, x + 14, y + 10, fill=color
        )
        self.w1 = canvas.create_oval(x - 12, y + 6, x - 4, y + 14, fill="black")
        self.w2 = canvas.create_oval(x + 4, y + 6, x + 12, y + 14, fill="black")

    def move(self, dx, dy):
        canvas.move(self.body, dx, dy)
        canvas.move(self.w1, dx, dy)
        canvas.move(self.w2, dx, dy)
        self.x += dx
        self.y += dy

    def destroy(self):
        canvas.delete(self.body)
        canvas.delete(self.w1)
        canvas.delete(self.w2)

# ---------------- STORAGE ----------------
cars_vertical = {x: [] for x in LANES_VERTICAL}
cars_horizontal = {y: [] for y in LANES_HORIZONTAL}

# ---------------- SPAWN ----------------
def spawn_vertical():
    lane = random.choice(LANES_VERTICAL)
    free = lane == LANES_VERTICAL[0]   # leftmost lane
    car = Car(lane, HEIGHT + 40, "vertical", free)
    cars_vertical[lane].append(car)
    root.after(1600, spawn_vertical)

def spawn_horizontal():
    lane = random.choice(LANES_HORIZONTAL)
    car = Car(-40, lane, "horizontal")
    cars_horizontal[lane].append(car)
    root.after(2200, spawn_horizontal)

# ---------------- ANIMATION ----------------
def animate():
    # Vertical cars
    for lane, lane_cars in cars_vertical.items():
        for i, car in enumerate(lane_cars):

            if i > 0 and car.y - lane_cars[i - 1].y < 35:
                continue

            # Free left turn
            if car.free_turn and not car.turned and car.y <= CENTER_Y:
                car.direction = "horizontal"
                car.turned = True

            if car.direction == "vertical":
                if current_green == "vertical" or car.y > STOP_LINE_Y:
                    car.move(0, -4)
            else:
                car.move(-4, 0)

            if car.y < -50 or car.x < -50:
                car.destroy()
                lane_cars.remove(car)

    # Horizontal cars
    for lane, lane_cars in cars_horizontal.items():
        for i, car in enumerate(lane_cars):

            if i > 0 and car.x - lane_cars[i - 1].x < 35:
                continue

            if current_green == "horizontal" or car.x < STOP_LINE_X:
                car.move(4, 0)

            if car.x > WIDTH + 50:
                car.destroy()
                lane_cars.remove(car)

    root.after(40, animate)

# ---------------- START ----------------
spawn_vertical()
spawn_horizontal()
animate()
switch_lights()

root.mainloop()
