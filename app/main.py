from fastapi import FastAPI

from app.routers import test as test_router
from app.routers import question as question_router
from app.routers import tag as tag_router

app = FastAPI()

app.include_router(test_router.router)
app.include_router(question_router.router)
app.include_router(tag_router.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}