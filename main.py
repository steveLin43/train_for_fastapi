import time
from fastapi import FastAPI, Request, HTTPException, status, BackgroundTasks
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from typing import Any, Dict, Union
from ws_api import websocket_endpoint

from routers.apiForm import router as form_router
from routers.apiJson import router as json_router
from config import Settings
from database import SessionLocal, engine
import models, schemas, crud
from log import logger

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    # call_next 用於處理進來的 api 路徑與參數
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

# 讓預期錯誤顯示 msg，非預期錯誤顯示 detail
class NewHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: Any = None, headers: Union[Dict[str, Any], None] = None, msg: str = None) -> None:
        super().__init__(status_code, detail, headers)
        if msg:
            self.msg = msg
        else:
            self.msg = detail

middleware = [
    Middleware(CustomHeaderMiddleware)
]

models.Base.metadata.create_all(bind=engine)

description = """
# 詳細說明
支援 **Markdwon**
"""

app = FastAPI(
    title="可自訂的文件標題",
    version="1.2.3",
    summary="這只是 Demo 用的",
    description=description,
    middleware=middleware
)

# 需要繞過 CORS 的來源網域
origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# 將文件的路由移除、不顯示
# app = FastAPI(openapi_url="")

# 增加文件根路由，用於調整網址、設定反向代理
# app = FastAPI(root_path="/ithome")

app.include_router(form_router, prefix="/api", tags=["api"])
app.include_router(json_router, prefix="/user", tags=["user"])
app.add_websocket_route("/ws", chat_socket)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code < 400:
           logger.info("Info")
        return response
    except Exception as e:     # 非預期的錯誤
        logger.error("Error:", e)     # 紀錄非預期的錯誤的 log
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

@app.exception_handler(NewHTTPException)
async def unicorn_exception_handler(request: Request, exc: NewHTTPException):
    logger.error("Error:", exc.msg)   # 紀錄可預期的錯誤的 log
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/")
async def root():
    logger.info('Test info log')
    try:
        print(a)
        b = 1 / 0
    except NameError as e:   # 可預期的錯誤
        raise NewHTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail="This is Value Error", msg=str(e))


settings = Settings()

@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/read_main")
async def read_main():
    return {"msg": "Hello World"}

# 監控啟動事件
@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}

def print_msg():
    time.sleep(5)
    print("Hello")

@app.get("/back")
async def back(background_tasks: BackgroundTasks):
    print("Hi")
    background_tasks.add_task(print_msg)
    return {"msg": "Hello World"}

