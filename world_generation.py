from matplotlib.pyplot import sca
from noise import pnoise1,pnoise2
import random
import noise
import numpy as np

class WorldGeneration():
    def __init__(self,seed):
        self.seed=seed
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
    
    def cave_map(self,threshold=0.1,width=200,height=300,coor_x=0,scale=40): #plus threshold est grand, plus y'a de grotte. Max: 1 | Min: 0        coor_x=la coordonnée x du début du chunk
        caves= np.zeros((width,height),dtype=bool) #on genere la map. En true et en false
        
        for x in range(width):
            coor_x+=1
            for y in range(height):
                noise_value = pnoise2(coor_x/scale,y/scale,octaves=4)
                caves[x,y] = noise_value>threshold # Plus c'est grand, moins y'a de grotte 

        return caves
#tests
if __name__=="__main__":
    world_generation=WorldGeneration(1000)
    cave_map = world_generation.cave_map()

    # Affichage des grottes
    import matplotlib.pyplot as plt
    plt.imshow(cave_map, cmap="gray")
    plt.show()
            