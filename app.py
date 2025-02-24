from turtle import width
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from world_generation import WorldGeneration
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

app=FastAPI(debug=True)
app.mount("/static",StaticFiles(directory="F:\\Ce PC\\Données(F:)\\Documents\\HYDROLIA\\Hydrolia"),name="static")

app.add_middleware( # pour CORS
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

@app.get("/")
async def serv_html():
    return FileResponse("F:\\Ce PC\\Données(F:)\\Documents\\HYDROLIA\\Hydrolia\\index.html")

@app.get("/favicon.ico")
async def serv_icon():
    return FileResponse("F:\\Ce PC\\Données(F:)\\Documents\\Hydrolia-Server\\favicon.ico")
async def generate_world(user_id: int, seed:int, coor_x: int):
    if user_id!=2001:
        raise HTTPException(status_code=403, detail="Your user_id is bad")
    world_generation = WorldGeneration(seed=seed)
    width=30
    
    relief_map = world_generation.relief(coor_x=coor_x,width=width)
    cave_map = world_generation.cave_map(coor_x=coor_x,width=width)
    print("Caca")
    bloc_map = world_generation.world_generation(relief_map,cave_map,coor_x=coor_x,width=width)
    return bloc_map #retourne bloc map jsonifié
    