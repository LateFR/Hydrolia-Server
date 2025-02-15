from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from world_generation import WorldGeneration
from fastapi import HTTPException
import world_generation

app=FastAPI(debug=True)
app.mount("/",StaticFiles(directory="C:\\Users\\lemax\\Lucas\\Hydrolia",html=True),name="static")

app.get("/{user_id}/world_generation")
async def generate_world(user_id: int, seed:int, coor_x: int):
    if user_id!=2001:
        return HTTPException(status_code=403, detail="user id is bad")
    world_generation = WorldGeneration(seed=seed)
    
    relief_map = world_generation.relief(coor_x=coor_x)
    cave_map = world_generation.cave_map(coor_x=coor_x)
    
    return world_generation.world_generation(relief_map,cave_map)
    