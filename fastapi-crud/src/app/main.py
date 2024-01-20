from fastapi import FastAPI
from fastapi.responses import RedirectResponse
app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse("/docs")
    
@app.get("/ping")
def pong():
    return {"ping": "pong!"}