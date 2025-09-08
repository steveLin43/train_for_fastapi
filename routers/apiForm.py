from fastapi import APIRouter, Form

router = APIRouter()

fake_items_db = [{"item_name": "Item-1"}, {"item_name": "Item-2"}, {"item_name": "Item-3"}]

# localhost:8000/items?skip=0
@router.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# localhost:8000/login1
# body 帶入 form-data 的內容
@router.post("/login1")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
