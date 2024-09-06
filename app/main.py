from fastapi import FastAPI
import logging
from app.routers import post, user, auth, vote
from app.database import engine, Base
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

print("Database Username:", settings.database_username)



# Set up logging before application setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers

app.include_router(post.router, prefix="/posts", tags=["Posts"])

app.include_router(user.router, prefix="/users", tags=["Users"])

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(vote.router, tags=["Votes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to my API!"}

@app.on_event("startup")
def startup_event():
    logger.info("Application startup")
    # This line will create all tables that do not exist yet
    Base.metadata.create_all(bind=engine)

@app.get("/test")
def test():
    return {"message": "Server is running"}


















