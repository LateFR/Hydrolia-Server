from turtle import width
from fastapi import FastAPI
import fastapi
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from world_generation import WorldGeneration
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

app = FastAPI(debug=True)
app.mount("/",StaticFiles(directory="C:\\Users\\lemax\\Lucas\\Hydrolia",html=True),name="static")
