from opensimplex import OpenSimplex
import random
import numpy as np

class WorldGeneration():
    def __init__(self, seed):
        self.seed = seed  # ne pas dépasser 500 000 en seed, pour que cave map fonctionne bien
        random.seed = seed  # set la seed
        self.global_x = 0
        self.MAX_HEIGHT = 200  # Hauteur du monde
        self.simplex = OpenSimplex(seed)

    def convert_y(self, y):
        return self.MAX_HEIGHT - y

    def relief(self, height_max=20, width=200, scale=50, coor_x=0):
        relief_map = []
        for x in range(coor_x, coor_x + width):
            noise_x = self.simplex.noise2(x / scale, self.seed)  # Utilisation de opensimplex
            height = int((noise_x + 1) / 2 * height_max)  # Normalisation [-1,1] -> [0, height_max]
            relief_map.append(height)
        return relief_map

    def bellow_relief(self, relief_map, coor_x=0, scale=20):
        if relief_map[coor_x] <= 1:
            return -1  # -1 pour garder au moins 1 bloc de séparation entre le sol et les caves

        height_max = relief_map[coor_x] - 1
        coor_x -= 200000
        noise_y = self.simplex.noise2(coor_x / scale, self.seed)
        height = int((noise_y + 1) / 2 * height_max) - 5
        return height

    def cave_map(self, threshold=0.3, width=200, height=85, coor_x=0, scale=40):
        height += 50  # On génère toujours en plus, afin de laisser de la marge
        offset_x = self.seed * 37.0
        offset_y = self.seed * 73.0

        caves = np.zeros((width, height), dtype=bool)
        for x in range(width):
            current_x = coor_x + x + offset_x
            for y in range(height):
                noise_value = self.simplex.noise2(current_x / scale, (y + offset_y) / scale)
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
                if not caves[x, y]:
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
    print(world_generation.world_generation(relief_map, cave_map))
    cave_visualisator(48086)