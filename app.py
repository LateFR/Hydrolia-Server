from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app=FastAPI(debug=True)
app.mount("/",StaticFiles(directory="C:\\Users\\lemax\\Lucas\\Hydrolia",html=True),name="static")
