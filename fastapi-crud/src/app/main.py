from fastapi import FastAPI
from .api import ping, root

app = FastAPI()

app.include_router(root.router)
app.include_router(ping.router)
    
