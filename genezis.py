import tkinter as tk
import random
import math

class Organism:
    def __init__(self, game_world, x, y):
        self.game_world = game_world
        self.canvas = game_world.canvas
        self.x = x
        self.y = y
        self.energy = 1000
        self.energy_idle_spending = random.randint(1, 2)
        self.energy_speed_spending = random.randint(5, 10)
        self.radius_of_sight = 50
        self.speed = 5
        self.random_move_chance = random.random()
        self.shape = self.canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill="blue")

    def move_towards_food(self):
        nearest_food = min(self.game_world.food, key=lambda f: distance(self.x, self.y, f.x, f.y))
        angle = math.atan2(nearest_food.y - self.y, nearest_food.x - self.x)
        new_x = int(self.x + self.speed * math.cos(angle))
        new_y = int(self.y + self.speed * math.sin(angle))
        
        # Ensure the new position is within the canvas boundaries
        new_x = max(0, min(new_x, self.game_world.width - 1))
        new_y = max(0, min(new_y, self.game_world.height - 1))

        self.canvas.coords(self.shape, new_x - 5, new_y - 5, new_x + 5, new_y + 5)
        self.x = new_x
        self.y = new_y
        self.energy -= self.speed * self.energy_speed_spending

    def move_randomly(self):
        angle = random.uniform(0, 2 * math.pi)
        new_x = int(self.x + self.speed * math.cos(angle))
        new_y = int(self.y + self.speed * math.sin(angle))
        
        # Ensure the new position is within the canvas boundaries
        new_x = max(0, min(new_x, self.game_world.width - 1))
        new_y = max(0, min(new_y, self.game_world.height - 1))

        self.canvas.coords(self.shape, new_x - 5, new_y - 5, new_x + 5, new_y + 5)
        self.x = new_x
        self.y = new_y
        self.energy -= self.speed * self.energy_speed_spending / 2

    def decide_move(self):
        food_in_sight = False

        for food in self.game_world.food:
            distance_to_food = distance(self.x, self.y, food.x, food.y)
            if distance_to_food <= self.radius_of_sight:
                food_in_sight = True
                break

        if food_in_sight:
            self.move_towards_food()
        elif random.random() < self.random_move_chance:
            self.move_randomly()
        else:
            self.energy -= self.speed * 2

    def is_dead(self):
        return self.energy <= 0

class Food:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.shape = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="green")

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

class GameWorld:
    def __init__(self, root, width=400, height=400):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.width = width
        self.height = height
        self.world_grid = [[[] for j in range(width)] for i in range(height)]
        self.organisms = []
        self.food = []

        for _ in range(20):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            organism = Organism(self, x, y)
            self.world_grid[x][y].append(organism)
            self.organisms.append(organism)

        food_item = self.spawn_food()
        self.world_grid[food_item[1]][food_item[2]].append(food_item[0])
        self.check_collision()
        self.spawn_food_periodically()
        self.update()
    def spawn_food_periodically(self):
        food_item = self.spawn_food()
        self.world_grid[food_item[1]][food_item[2]].append(food_item[0])
        self.check_collision()
        self.root.after(100, self.spawn_food_periodically)
    def check_collision(self):
        item_count = 0
        for i in self.world_grid:
            for j in i:
                element = j
                if len(j) > 0: item_count += 1
                if len(j) > 1:
                    is_collision_with_food = False
                    is_first_organism = False
                    _first_organism = None
                    _food_item =None
                    for item in j:
                        if type(item) == Food:
                            is_collision_with_food = True
                            _food_item = item
                        else:
                            if not is_first_organism:
                                is_first_organism = True
                                _first_organism = item
                    
                    print(f"COLLISION {len(j)}")
                    if is_collision_with_food and is_first_organism:
                        print(f"NUMNUMNUM {_first_organism.energy} {_food_item.shape}")
                        _first_organism.energy += 100
                        self.canvas.delete(_food_item.shape)
                        self.food.remove(_food_item)

        print(f"item_count {item_count}")

    def spawn_food(self):
        for _ in range(10):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            food = Food(self.canvas, x, y)
            self.food.append(food)
            return [food, x, y]

    def update(self):
        self.world_grid = [[[] for j in range(self.width)] for i in range(self.height)]
        
        for _food in self.food:
            self.world_grid[_food.x][_food.y].append( _food)
        for organism in self.organisms:
            if organism.is_dead():
                self.canvas.delete(organism.shape)
                self.organisms.remove(organism)
            else:
                self.world_grid[organism.x][organism.y].append(organism)
                organism.decide_move()
                
                # Ensure organisms do not move beyond canvas boundaries
                organism.x = max(0, min(organism.x, self.width - 1))
                organism.y = max(0, min(organism.y, self.height - 1))
                
        self.check_collision()
        self.root.after(100, self.update)

root = tk.Tk()
game_world = GameWorld(root)
root.mainloop()
