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
        self.MAX_HEIGHT = 400 #Hauteur du monde
        
    def convert_y(self,y): #On convertit y car phaser fonctionne sur des coordonnées canvas html et que 0=le haut du monde. Donc si y=390, alors on le trasforme en y=10 (si max_height=400)
        return self.MAX_HEIGHT- y
    
    def relief(self,height_max=30,width=200,scale=20,coor_x=0): #height_max=hauteur max    width=largeur du chunk(en blocs)  scale=echelle du bruit (plus c'est grand, plus le terrain est lisse)  coor_x=la coordonnée x du début du chunk
        
        relief_map=[]
        for x in range(width):
            noise_x = pnoise1(coor_x/scale, octaves=4) #coor_x pour garder la continuité dans les chunks. Ils faut mettre à jour coor_x
            coor_x+=1
            
            height = int((noise_x + 1) / 2 * height_max)  # Normalisation [-1,1] → [0, height_max]
            relief_map.append(height)
        
        return relief_map
    
    def bellow_relief(self,relief_map,coor_x=0,scale=20):
        if relief_map[coor_x]<=1: #on ne génere pas si il est la hauteur inférieur ou égale a 1
            return -1 # -1 pour garder au moins 1 bloc de séparation entre le sol est les caves
        
        height_max = relief_map[coor_x]-1 #on empeche le sous relief de dépasser le relief
        
        coor_x-=200000 #pour garder une continuité sans pour autant que le sous relief soit identique au relief
        
        noise_y = pnoise1(coor_x/scale, octaves=4)
        
        
        height = int((noise_y + 1) / 2 * height_max)-5  # Normalisation [-1,1] → [0, height_max] # -5 = 5 bloc de marge pour être sur d'avoir un sol
        
        return height
        
        
    
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
    
    def world_generation(self,relief_map,caves,biome_map=None,width=200,height_cave=200):
        world={}
        i=0
        for x in range(width):
            i+=1
            #biome = biome_map[x]
            biome="plain"
            
            height = relief_map[x]
            
            sub_relief = self.bellow_relief(relief_map,coor_x=x)
            
            for y in range(height_cave+sub_relief): #les caves iront de y0 a y200. Elle sont doivent s'arreter à sub relief
                if caves[x,y] == True: #si jamais y'a pas de caves on ajoute un bloc de stone
                    world[i] = ["stone",(x,self.convert_y(y))] #On adapte la coordonnée y  pour phaser
                else: #sinon, un bloc d'air
                    world[i] = ["air",(x,self.convert_y(y))] #On adapte la coordonnée y  pour phaser
                i+=1
            
            for y in range(height): #sur les 20 blocs accordés au relief, on met des blocs custom au biome. Le "sous relief" qui définit la frontière entre la partie cave et le sol
                y+=200+sub_relief #on rajoute 200 à y puisqu'on est à 200 de hauteur et on fait en fonction du sous relief
                
                if biome=="plain":
                    world[i] = ["dirt",(x,self.convert_y(y))] #On adapte la coordonnée y  pour phaser
                i+=1
            
        return world
                        
                    
    
#tests
if __name__=="__main__":
    
    def cave_visualisator(seed):
        world_generation=WorldGeneration(seed)
        cave_map = world_generation.cave_map()
        
        # Affichage des grottes
        import matplotlib.pyplot as plt
        plt.imshow(cave_map, cmap="gray")
        plt.show()
    
    world_generation = WorldGeneration(seed=5)
    
    relief_map = world_generation.relief(coor_x=0)
    cave_map = world_generation.cave_map(coor_x=0)
    
    print(world_generation.world_generation(relief_map,cave_map))