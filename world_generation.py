from fastapi.background import P
from matplotlib.pyplot import sca
from noise import pnoise1,pnoise2
import random
import noise
import numpy as np

class WorldGeneration():
    def __init__(self,seed):
        self.seed=seed #ne pas dépasser 500 000 en seed, pour que cave map fonctionne bien
        random.seed=seed #set la seed
        self.global_x=0
    
    def relief(self,height_max=300,width=200,scale=20,coor_x=0): #height_max=hauteur max    width=largeur du chunk(en blocs)  scale=echelle du bruit (plus c'est grand, plus le terrain est lisse)  coor_x=la coordonnée x du début du chunk
        
        relief_map=[]
        for x in range(width):
            noise_x = pnoise1(coor_x/scale, octaves=4) #self.global_x pour garder la contionuité dans les chunks. Ils faut mettre à jour global_x
            coor_x+=1
            
            height = int((noise_x + 1) / 2 * height_max)  # Normalisation [-1,1] → [0, height_max]
            relief_map.append(height)
        
        return relief_map
    
    def cave_map(self, threshold=0.1, width=200, height=300, coor_x=0, scale=40):
        # Calcul d'un décalage en fonction de la seed.
        # Ces coefficients (ici 37 et 73) sont choisis arbitrairement pour "mélanger" la seed.
        offset_x = self.seed * 37.0  
        offset_y = self.seed * 73.0  

        caves = np.zeros((width, height), dtype=bool)
        
        # On parcourt chaque colonne (x)
        for x in range(width):
            # La coordonnée x actuelle intègre la position dans le chunk et le décalage de la seed
            current_x = coor_x + x + offset_x
            # Pour chaque ligne (y)
            for y in range(height):
                # On ajoute également le décalage sur l'axe y
                noise_value = pnoise2(current_x / scale, (y + offset_y) / scale, octaves=4)
                caves[x, y] = noise_value > threshold

        return caves
    
#tests
if __name__=="__main__":
    
    def cave_visualisator(seed):
        world_generation=WorldGeneration(seed)
        cave_map = world_generation.cave_map()

        # Affichage des grottes
        import matplotlib.pyplot as plt
        plt.imshow(cave_map, cmap="gray")
        plt.show()