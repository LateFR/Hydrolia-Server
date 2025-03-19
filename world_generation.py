from fastapi.background import P
from opensimplex import noise2, noise3
import random
import numpy as np

class WorldGeneration():
    def __init__(self, seed):
        self.seed = seed  # ne pas dépasser 500 000 en seed, pour que cave map fonctionne bien
        random.seed = seed  # set la seed
        self.global_x = 0
        self.MAX_HEIGHT = 200  # Hauteur du monde
    
    def convert_y(self, y):
        return self.MAX_HEIGHT - y
    
    def relief(self, height_max=20, width=200, scale=50, coor_x=0):
        relief_map = []
        for x in range(coor_x, coor_x + width):
            noise_x = noise2(x / scale, self.seed)  # Utilisation d'opensimplex
            height = int((noise_x + 1) / 2 * height_max)  # Normalisation [-1,1] → [0, height_max]
            relief_map.append(height)
        return relief_map
    
    def bellow_relief(self, relief_map, coor_x=0, scale=20):
        if relief_map[coor_x] <= 1:
            return -1
        height_max = relief_map[coor_x] - 1
        coor_x -= 200000  # Garde une continuité sans que le sous relief soit identique au relief
        noise_y = noise2(coor_x / scale, self.seed)
        height = int((noise_y + 1) / 2 * height_max) - 5  # Marge de 5 blocs
        return height
    
    def cave_map(self, threshold=0.3, width=200, height=85, coor_x=0, scale=40):
        height += 50
        offset_x = self.seed * 37.0  
        offset_y = self.seed * 73.0  
        caves = np.zeros((width, height), dtype=bool)
        for x in range(width):
            current_x = coor_x + x + offset_x
            for y in range(height):
                noise_value = noise3(current_x / scale, (y + offset_y) / scale, self.seed)
                caves[x, y] = noise_value > threshold
        return caves
    
    def world_generation(self, relief_map, caves, coor_x, biome_map=None, width=200, height_cave=85):
        world = {}
        i = 0
        for x in range(width):
            real_x = coor_x + x
            biome = "plain"
            height = relief_map[x]
            sub_relief = self.bellow_relief(relief_map, coor_x=x)
            for y in range(height_cave + sub_relief):
                if caves[x, y] == False:
                    world[i] = ["stone", (real_x, self.convert_y(y))]
                else:
                    world[i] = ["air", (real_x, self.convert_y(y))]
                i += 1
            for y in range(height):
                y += height_cave + sub_relief
                if biome == "plain":
                    world[i] = ["dirt", (real_x, self.convert_y(y))]
                i += 1
        return world

if __name__ == "__main__":
    def cave_visualisator(seed):
        world_generation = WorldGeneration(seed)
        cave_map = world_generation.cave_map()
        import matplotlib.pyplot as plt
        plt.imshow(cave_map, cmap="gray")
        plt.show()
    
    world_generation = WorldGeneration(seed=5)
    relief_map = world_generation.relief(coor_x=0)
    cave_map = world_generation.cave_map(coor_x=0)
    print(world_generation.world_generation(relief_map, cave_map, coor_x=0))
    cave_visualisator(48086)