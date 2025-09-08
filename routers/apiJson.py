from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    username: str
    age: int

class UserDetail(BaseModel):
    name: str
    age: int
    email: str
    phone: str

# class UserDetail(User):
#     email: str
#     phone: str


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

##### ============================================================ #####
# 直接回傳物件
@router.post("/user")
async def create_user(user: User) -> User:
    return user

@router.get("/users")
async def read_users() -> list[User]:
    return [
        User(name="John Doe", age=18),
        User(name="Ithome Ironman", age=22),
    ]

fake_db = [UserDetail(name="John Doe", age=18, email="johndoe@gmail.com", phone="0911555666"),
           UserDetail(name="Ithome Ironman", age=22, email="ithome@gmail.com", phone="0911777888")]
# 使用 pydantic model，不僅可將回傳自動轉為 json，還可以藉由指定回傳的 Model 類型去過濾資訊
@router.get("/users")
async def read_users() -> list[User]:
    return fake_db

@router.get("/admin/users")
async def read_users() -> list[UserDetail]:
    return fake_db