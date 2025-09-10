import time
from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session

from routers.apiForm import router as form_router
from routers.apiJson import router as json_router
from config import Settings
from database import SessionLocal, engine
import models, schemas, crud

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    # call_next 用於處理進來的 api 路徑與參數
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}


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
