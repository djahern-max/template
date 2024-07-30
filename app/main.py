from fastapi import FastAPI
from app.routers import user, auth  # Adjust import based on your project structure

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/test")
def test():
    return {"message": "Test route is working"}









