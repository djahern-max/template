from fastapi import APIRouter

print("Test router initialized")
router = APIRouter(
    prefix="/test",
    tags=["Test"]
)

@router.get("/", status_code=200)
def read_test():
    return {"message": "Test router is working!"}
