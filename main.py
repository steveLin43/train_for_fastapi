from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

fake_items_db = [{"item_name": "Item-1"}, {"item_name": "Item-2"}, {"item_name": "Item-3"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}

# localhost:8000/items?skip=0
@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# localhost:8000/login1
# body 帶入 form-data 的內容
@app.post("/login1")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


class User(BaseModel):
    username: str
    password: str

# localhost:8000/login2
# body 帶入 json 的內容
@app.post("/login2")
async def login(user: User):
    return {"username": user.username}