from fastapi import FastAPI
from app.routers import user  # adjust import based on your project structure

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])

@app.get("/test")
def test():
    return {"message": "Test route is working"}









