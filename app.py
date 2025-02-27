import hashlib
from turtle import width
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from world_generation import WorldGeneration
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import os

app=FastAPI(debug=True)
app.mount("/static",StaticFiles(directory="C:\\Users\\lemax\\Lucas\\Hydrolia"),name="static")

app.add_middleware( # pour CORS
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

@app.get("/")
async def serv_html():
    return FileResponse("C:\\Users\\lemax\\Lucas\\Hydrolia\\index.html")

@app.get("/favicon.ico")
async def serv_icon():
    return FileResponse("C:\\Users\\lemax\\Lucas\\Hydrolia-Server\\favicon.ico")

@app.post("/redeploy/front-end")
async def redeploy_front_end(secret_key: str):
    SECRET_HASHED = "32a73dd686c90fde4390a1b9e846bead58c4846987af2178ce9eb81cd3eed864b7a29b301c30d8007001b5f72d867e969d8f58d1fb261371e6e0058120888113"
    secret_key_hashed = hashlib.sha512(secret_key.encode()).hexdigest()
    
    if(secret_key_hashed!=SECRET_HASHED):
        return {"error":"Unauthorized"}
    
    os.system("cd C:\\Users\\lemax\\Lucas\\Hydrolia\\Hydrolia-Production && git pull")

@app.get("/{user_id}/world_generation/")
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
    