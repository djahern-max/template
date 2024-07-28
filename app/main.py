from fastapi import FastAPI
import logging
from app.routers import post, user, auth

# Set up logging before application setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include routers
app.include_router(post.router, prefix="/posts", tags=["Posts"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to my API!"}

@app.on_event("startup")
def startup_event():
    logger.info("Application startup")








