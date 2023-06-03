from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import TagNotFoundException
from app.routers import question as question_router
from app.routers import tag as tag_router
from app.routers import test as test_router

app = FastAPI()

app.include_router(test_router.router)
app.include_router(question_router.router)
app.include_router(tag_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Doing this instead of throwing HTTPException from question repository
# Could go either way or make TagNotFoundException extend HTTPException
@app.exception_handler(TagNotFoundException)
async def tag_not_found_exception_handler(request, e: TagNotFoundException):
    return JSONResponse(content={"details": str(e)}, status_code=400)
