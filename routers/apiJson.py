from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

# localhost:8000/login2
# body 帶入 json 的內容
@router.post("/login2")
async def login(user: User):
    return {"username": user.username}


# Restful
@router.get("/data", summary="test for long description", description="long description")
async def root():
    """
    # Markdwon
    ## Hello World

    Cool!
    - I can write markdwon message here
    - It's **awesome**
    """
    return {"message": "Hello World"}

@router.post("/data")
async def root():
    return {"message": "Hello World"}