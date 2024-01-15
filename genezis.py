import tkinter as tk
import random

class Organism:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.energy = 50
        self.moves_since_last_meal = 0
        self.id = canvas.create_rectangle(x, y, x+20, y+20, fill="blue")

    def eat(self):
        food_energy = random.randint(5, 20)
        self.energy += food_energy
        self.moves_since_last_meal = 0

    def move_towards_food(self, food_x, food_y):
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        food_distance = ((food_x - (x1 + x2) / 2) ** 2 + (food_y - (y1 + y2) / 2) ** 2) ** 0.5
        if food_distance > 0:
            move_ratio = min(5, food_distance) / food_distance
            dx = move_ratio * (food_x - (x1 + x2) / 2)
            dy = move_ratio * (food_y - (y1 + y2) / 2)
            self.canvas.move(self.id, dx, dy)

    def move(self):
        if  self.energy >= 5 : 
            self.energy -= 5
            self.moves_since_last_meal += 1
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            self.canvas.move(self.id, dx, dy)
            frm = tk.Frame(root, padding=10)
            frm.grid()
            tk.Label(frm, text=self.energy).grid(column=0, row=0)
        else :
            return None            
    def reproduce(self, x, y):
        if self.energy >= 60 and self.moves_since_last_meal == 0:
            child = Organism(self.canvas, x, y)
            self.energy -= 30
            return child
        else:
            return None

    def check_death(self):
        return self.moves_since_last_meal >= 10

class Food:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x, self.y = x, y
        self.id = canvas.create_rectangle(x, y, x+10, y+10, fill="green")

    def respawn(self):
        pass  # Не перемещаем еду, чтобы она оставалась на месте

class SimulationApp:
    def __init__(self, root, width, height):
        self.root = root
        self.root.title("Life Simulation")
        self.canvas = tk.Canvas(root, width=width, height=height, bg="white")
        self.canvas.pack()

        self.population = []
        self.food = Food(self.canvas, random.randint(0, width-10), random.randint(0, height-10))

        # Создаем начальную популяцию
        for _ in range(5):
            x = random.randint(0, width-20)
            y = random.randint(0, height-20)
            organism = Organism(self.canvas, x, y)
            self.population.append(organism)

        self.running = False

        start_button = tk.Button(root, text="Start Simulation", command=self.start_simulation)
        start_button.pack()

        stop_button = tk.Button(root, text="Stop Simulation", command=self.stop_simulation)
        stop_button.pack()

    def start_simulation(self):
        self.running = True
        self.run_simulation()

    def stop_simulation(self):
        self.running = False

    def run_simulation(self):
        if not self.running:
            return :

        new_population = []

        for organism in self.population:
            organism.move_towards_food(self.food.x + 5, self.food.y + 5)
            organism.move()
            organism.eat()

            if organism.check_death():
                self.canvas.delete(organism.id)
            else:
                new_population.append(organism)
            

        self.population = new_population

        self.root.update()
        self.root.after(500, self.run_simulation)  # вызываем run_simulation через 2 секунды

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root, 400, 400)
    root.mainloop()
