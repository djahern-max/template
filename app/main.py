from fastapi import FastAPI
from app.routers import post, user
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.include_router(post.router, prefix="/posts")
app.include_router(user.router, prefix="/users")

@app.get("/")
def read_root():
    return {"message": "Welcome to my API!"}

app.include_router(post.router, prefix="/posts")

@app.on_event("startup")
def startup_event():
    logger.info("Application startup")







