from fastapi import FastAPI
from app.api import brainstorming, content_map

app = FastAPI(title="Content App V2 API")

app.include_router(brainstorming.router)
app.include_router(content_map.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Content App V2 API"}
