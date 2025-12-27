import tkinter as tk

# ---------------- WINDOW ----------------
WIDTH = 600
HEIGHT = 400

root = tk.Tk()
root.title("Traffic Simulation")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# ---------------- LANE ----------------
canvas.create_line(300, 0, 300, HEIGHT, width=4)

# ---------------- CAR CLASS ----------------
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Car body
        self.body = canvas.create_rectangle(
            x, y, x + 60, y + 30, fill="blue"
        )

        # Wheels
        self.wheel1 = canvas.create_oval(
            x + 5, y + 25, x + 20, y + 40, fill="black"
        )
        self.wheel2 = canvas.create_oval(
            x + 40, y + 25, x + 55, y + 40, fill="black"
        )

    def move(self):
        canvas.move(self.body, 0, -5)
        canvas.move(self.wheel1, 0, -5)
        canvas.move(self.wheel2, 0, -5)

        self.y -= 5

# ---------------- CREATE CAR ----------------
car = Car(270, 350)

# ---------------- ANIMATION LOOP ----------------
def animate():
    if car.y > -50:
        car.move()
        root.after(200, animate)

animate()
root.mainloop()
