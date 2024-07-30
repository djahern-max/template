from fastapi import FastAPI
from app.routers import user, auth, post  # Adjust import based on your project structure

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])

@app.get("/test")
def test():
    return {"message": "Test route is working"}

from app.database import engine, Base
from app import models

# Ensure all models are imported so that Base.metadata.create_all can access them
models.Base.metadata.create_all(bind=engine)









