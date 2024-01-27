from vpython import *
from vpython import color
import random
import math
import numpy as np

class Organism:
    def __init__(self, game_world, x, y, z, national_id, parent=None):
        self.game_world = game_world
        self.x, self.y, self.z = x, y, z

        if parent:
            # Inherit characteristics from the parent
            self.national_id = parent.national_id
            self.basic_energy_amount = parent.basic_energy_amount
            self.speed = parent.speed
            self.radius_of_sight = parent.radius_of_sight
            self.energy_idle_spending = parent.energy_idle_spending
            self.energy_run_spending = parent.energy_run_spending
            self.energy_find_walk_spending = parent.energy_find_walk_spending
            self.random_move_chance = parent.random_move_chance
            self.attack_chance = parent.attack_chance
            self.attack_radius = parent.attack_radius
            self.attack_damage = parent.attack_damage
            self.color = parent.color
        else:
            # Randomly set characteristics for a new organism
            self.national_id = national_id
            self.basic_energy_amount = random.randint(100, 200)
            self.speed = random.randint(2, 7)
            self.radius_of_sight = random.randint(10, 70)
            self.energy_idle_spending = random.randint(1, 2)
            self.energy_run_spending = random.randint(1, 10)
            self.energy_find_walk_spending = random.randint(2, 4)
            self.random_move_chance = random.random()
            self.attack_chance = random.random()
            self.attack_radius = random.randint(1, 5)
            self.attack_damage = random.randint(1,30)
            self.color = random.choice([vector(0.6, 0.4, 0.2), vector(0, 0, 1), vector(0.6, 0.2, 0.6),
                            vector(0, 1, 1), vector(1, 0.8, 0), vector(1, 0, 1)])
            if hasattr(color, 'rgb_to_vector'):
                self.shape = sphere(pos=vector(x, y, z), radius=5, color=color.rgb_to_vector(self.color))
            else:
                self.shape = sphere(pos=vector(x, y, z), radius=5, color=self.color)

        self.energy = self.basic_energy_amount
        self.create_shape()
        #self.shape = sphere(pos=vector(x, y, z), radius=5, color=self.color)


    def move_towards_food(self):
        nearest_food = min(self.game_world.food, key=lambda f: np.linalg.norm(np.array([self.x, self.y, self.z]) - f.position))
        angle = math.atan2(nearest_food.position[1] - self.y, nearest_food.position[0] - self.x)
        new_x = self.x + self.speed * math.cos(angle)
        new_y = self.y + self.speed * math.sin(angle)
        new_z = self.z + self.speed * math.cos(angle)

        new_grid_x = round(new_x / self.game_world.cell_size)
        new_grid_y = round(new_y / self.game_world.cell_size)
        new_grid_z = round(new_z / self.game_world.cell_size)

        if 0 <= new_x < self.game_world.width and 0 <= new_y < self.game_world.height and 0 <= new_z < self.game_world.depth:
            if not self.game_world.is_occupied(new_grid_x, new_grid_y, new_grid_z):
                self.update_position(new_x, new_y, new_z)

                if np.linalg.norm(np.array([new_x, new_y, new_z]) - nearest_food.position) < self.game_world.cell_size:
                    self.eat_food(nearest_food)

        # Calculate the grid indices for the new position
        new_grid_x = round(new_x / self.game_world.cell_size)
        new_grid_y = round(new_y / self.game_world.cell_size)
        new_grid_z = round(new_z / self.game_world.cell_size)

        # Check if the new position is within the canvas boundaries
        if 0 <= new_x < self.game_world.width and 0 <= new_y < self.game_world.height and 0 <= new_z < self.game_world.depth:
            # Check if the new position is occupied by another organism or food
            if not self.game_world.is_occupied(new_grid_x, new_grid_y, new_grid_z):
                self.update_position(new_x, new_y, new_z)

                # Check if the organism is adjacent to the food
                if np.linalg.norm(np.array([new_x, new_y, new_z]) - nearest_food.position) < self.game_world.cell_size:
                    self.eat_food(nearest_food)
                    
    def eat_food(self, food):
        self.energy += food.food_value
        food.shape.visible = False

        if food in self.game_world.food:
            self.game_world.food.remove(food)

        # Reproduce if energy is more than twice the basic value
        if self.energy > 2 * self.basic_energy_amount:
            self.reproduce()


    def move_randomly(self):
        angle = random.uniform(0, 2 * math.pi)
        new_x = self.x + self.speed * math.cos(angle)
        new_y = self.y + self.speed * math.sin(angle)
        new_z = self.z + self.speed * math.sin(angle)
        self.update_position(new_x, new_y, new_z)

        angle = random.uniform(0, 2 * math.pi)
        new_x = round(self.x + self.speed * math.cos(angle))
        new_y = round(self.y + self.speed * math.sin(angle))
        new_z = round(self.z + self.speed * math.sin(angle))
        self.update_position(new_x, new_y, new_z)
        
    def create_shape(self):
        if hasattr(color, 'rgb_to_vector'):
            self.shape = sphere(pos=vector(self.x, self.y, self.z), radius=5, color=color.rgb_to_vector(self.color))
        else:
            self.shape = sphere(pos=vector(self.x, self.y, self.z), radius=5, color=self.color)

    def reproduce(self):
        # Create a new organism near the current one with the same characteristics
        new_x = self.x + random.randint(-5, 5)
        new_y = self.y + random.randint(-5, 5)
        new_z = self.z + random.randint(-5, 5)

        # Ensure the new position is within the canvas boundaries
        new_x = max(0, min(new_x, self.game_world.width - 1))
        new_y = max(0, min(new_y, self.game_world.height - 1))
        new_z = max(0, min(new_z, self.game_world.depth - 1))

        # Check if the new position is occupied by another organism or food
        if not self.game_world.is_occupied(round(new_x / self.game_world.cell_size),
                                        round(new_y / self.game_world.cell_size),
                                        round(new_z / self.game_world.cell_size)):
            new_organism = Organism(self.game_world, int(new_x), int(new_y), int(new_z), self.national_id, parent=self)
            self.game_world.world_grid[round(new_x / self.game_world.cell_size)][round(new_y / self.game_world.cell_size)][round(new_z / self.game_world.cell_size)].append(
                new_organism)
            self.game_world.organisms.append(new_organism)
            #print(f"Reproducing! Parent energy: {self.energy}, Child energy: {new_organism.energy}")


    def update_position(self, new_x, new_y, new_z):
        new_x = max(0, min(new_x, self.game_world.width - 1))
        new_y = max(0, min(new_y, self.game_world.height - 1))
        new_z = max(0, min(new_z, self.game_world.depth - 1))

        new_grid_x = round(new_x / self.game_world.cell_size)
        new_grid_y = round(new_y / self.game_world.cell_size)
        new_grid_z = round(new_z / self.game_world.cell_size)

        if not self.game_world.is_occupied(new_grid_x, new_grid_y, new_grid_z):
            self.x, self.y, self.z = new_x, new_y, new_z
            self.shape.pos = vector(new_x, new_y, new_z)

    def decide_move(self):
        food_in_sight = False
        organism_in_sight = False
        nearest_food = None
        nearest_organism = None

        for food in self.game_world.food:
            distance_to_food = distance(self.x, self.y, self.z, food.position[0], food.position[1], food.position[2])
            if distance_to_food <= self.radius_of_sight:
                food_in_sight = True
                if nearest_food is None or distance_to_food < distance(self.x, self.y, self.z, nearest_food.position[0], nearest_food.position[1], nearest_food.position[2]):
                    nearest_food = food

        for organism in self.game_world.organisms:
            if organism.national_id != self.national_id and organism.color != self.color:
                distance_to_organism = distance(self.x, self.y, self.z, organism.x, organism.y, organism.z)
                if distance_to_organism <= self.radius_of_sight:
                    organism_in_sight = True
                    if nearest_organism is None or distance_to_organism < distance(self.x, self.y, self.z, nearest_organism.x, nearest_organism.y, nearest_organism.z):
                        nearest_organism = organism

        if food_in_sight:
            self.move_towards_food()
            self.energy -= self.speed * self.energy_run_spending
        elif organism_in_sight and random.random() < self.attack_chance:
            self.attack_nearest_organism(nearest_organism)
        elif random.random() < self.random_move_chance:
            self.move_randomly()
            self.energy -= self.speed * self.energy_find_walk_spending
        else:
            self.energy -= self.energy_idle_spending

    def attack_nearest_organism(self, target_organism):
        distance_to_target = distance(self.x, self.y, self.z, target_organism.x, target_organism.y, target_organism.z)
        color_tuple = (target_organism.color.x, target_organism.color.y, target_organism.color.z)

        if distance_to_target < self.attack_radius:
            target_organism.energy -= self.attack_damage
            if target_organism.is_dead():
                self.game_world.dead_organisms_count += 1
                self.game_world.dead_by_attack_count += 1

                if color_tuple not in self.game_world.dead_colors_counter:
                    self.game_world.dead_colors_counter[color_tuple] = 1
                else:
                    self.game_world.dead_colors_counter[color_tuple] += 1

                target_organism.shape.visible = False
                self.game_world.organisms.remove(target_organism)
                self.game_world.mark_fight_location(target_organism.x, target_organism.y, target_organism.z)

                print(f"attack_nearest_organism {self.color} ---->>>[DEAD] {target_organism.color}")
            else:
                self.energy -= target_organism.attack_damage
                if self.is_dead():
                    self.game_world.dead_organisms_count += 1
                    self.game_world.dead_by_attack_count += 1

                    if color_tuple not in self.game_world.dead_colors_counter:
                        self.game_world.dead_colors_counter[color_tuple] = 1
                    else:
                        self.game_world.dead_colors_counter[color_tuple] += 1

                    target_organism.shape.visible = False
                    self.game_world.organisms.remove(self)
                    self.game_world.mark_fight_location(self.x, self.y, self.z)
                    print(f"attack_nearest_organism {self.color} [DEAD] ---->>> {target_organism.color}")
                else:
                    print(f"attack_nearest_organism {self.color} {self.energy}---->>> {target_organism.color} {target_organism.energy}")
    def is_dead(self):
        return self.energy <= 0

class Food:
    def __init__(self, game_world, x, y, z):
        self.food_value = random.randint(50, 100)
        self.position = np.array([x, y, z])
        self.shape = sphere(pos=vector(x, y, z), radius=3, color=color.green)


def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

class GameWorld:
    def __init__(self, width=400, height=400, depth=400, cell_size=10):
        self.width = width
        self.height = height
        self.depth = depth
        self.world_grid = [[[[] for k in range(depth)] for j in range(width)] for i in range(height)]
        self.organisms = []
        self.food = []
        self.cell_size = cell_size

        self.dead_organisms_count = 0
        self.dead_by_attack_count = 0
        self.dead_by_age_count = 0
        self.dead_by_fight_count = 0
        self.dead_by_starvation_count = 0
        
        self.dead_colors_counter = {
            "brown": 0,
            "blue": 0,
            "purple": 0,
            "cyan": 0,
            "gold": 0,
            "magenta": 0
        }

        for i in range(20):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            z = random.randint(0, depth - 1)
            organism = Organism(self, x, y, z, i)
            self.world_grid[x][y][z].append(organism)
            self.organisms.append(organism)

        self.spawn_food_periodically()
        self.update()

    def is_occupied(self, grid_x, grid_y, grid_z):
        return len(self.world_grid[grid_x][grid_y][grid_z]) > 0

    def spawn_food_periodically(self):
        self.spawn_food()
        while True:
            #rate(1)
            self.update()

    def keydown(self, evt):
        self.keyup[evt.key] = 1

    def keyup(self, evt):
        self.keyup[evt.key] = 0

    def mousemove(self, evt):
        pass

    def mousedown(self, evt):
        pass

    def mouseup(self, evt):
        pass

    def spawn_food(self):
        food_to_spawn = random.randint(5, 20)
        for _ in range(food_to_spawn):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            z = random.randint(0, self.depth - 1)
            food = Food(self, x, y, z)

            food.position = np.array([x, y, z])

            self.world_grid[x][y][z].append(food)
            self.food.append(food)
        self.update()

    def update(self):
        self.world_grid = [[[[] for k in range(self.depth)] for j in range(self.width)] for i in range(self.height)]

        # Process organisms
        living_organisms = []
        for organism in self.organisms:
            if not organism.is_dead():
                self.world_grid[int(organism.x)][int(organism.y)][int(organism.z)].append(organism)
                organism.decide_move()

                # Ensure organisms do not move beyond canvas boundaries
                organism.x = max(0, min(organism.x, self.width - 1))
                organism.y = max(0, min(organism.y, self.height - 1))
                organism.z = max(0, min(organism.z, self.depth - 1))
                living_organisms.append(organism)
            else:
                organism.shape.visible = False
        # Check collision after processing all organisms
        self.update_counters()
        self.spawn_food()
        # Update the list of living organisms
        self.organisms = living_organisms


    def update_counters(self):
        organism_count = len(self.organisms)
        food_count = len(self.food)

        print(f"Organisms: {organism_count}, Dead organisms: {self.dead_organisms_count}, Dead by attack: {self.dead_by_attack_count}, Dead by starvation: {self.dead_by_starvation_count}, Dead by fight: {self.dead_by_fight_count}, Food: {food_count}")

    def restart_world(self):
        print("################################################################")
        print("#")
        print("#")
        print("#")
        print("#")
        print("WORLD RESTARTING")
        print("#")
        print("#")
        print("#")
        print("#")
        print("################################################################")
        # Destroying current organisms and food
        for organism in self.organisms:
            organism.shape.visible = False
        self.organisms = []

        for food_item in self.food:
            food_item.shape.visible = False
        self.food = []

        # Creating new organisms and food
        for i in range(20):
            x = random.randint(0, self.width - 1)


            y = random.randint(0, self.height - 1)
            z = random.randint(0, self.depth - 1)
            organism = Organism(self, x, y, z, i)
            self.world_grid[x][y][z].append(organism)
            self.organisms.append(organism)

        self.spawn_food_periodically()

        # Reset counters
        self.dead_organisms_count = 0
        self.dead_by_attack_count = 0
        self.dead_by_age_count = 0
        self.dead_by_fight_count = 0
        self.dead_by_starvation_count = 0

        self.dead_colors_counter = {
            "brown": 0,
            "blue": 0,
            "purple": 0,
            "cyan": 0,
            "gold": 0,
            "magenta": 0
        }

        self.update()

    def mark_fight_location(self, x, y, z):
        box(pos=vector(x, y, z), length=1, height=1, width=1, color=color.red)



# Создаем мир
scene = canvas(width=1920, height=1080)
world = GameWorld(width=60, height=60, depth=60, cell_size=10)
scene.userpan = True
scene.userzoom = True
scene.userspin = True
while True:
    rate(60)  # Число кадров в секунду, можно изменить по вашему усмотрению
    world.update()
