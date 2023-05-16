from fastapi import FastAPI

from app.routers import test

app = FastAPI()

app.include_router(test.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}