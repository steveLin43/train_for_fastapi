from fastapi import FastAPI

from routers.apiForm import router as form_router
from routers.apiJson import router as json_router

description = """
# 詳細說明
支援 **Markdwon**
"""

app = FastAPI(
    title="可自訂的文件標題",
    version="1.2.3",
    summary="這只是 Demo 用的",
    description=description
)

# 將文件的路由移除、不顯示
# app = FastAPI(openapi_url="")

# 增加文件根路由，用於調整網址、設定反向代理
# app = FastAPI(root_path="/ithome")

app.include_router(form_router, prefix="/api", tags=["api"])
app.include_router(json_router, prefix="/user", tags=["user"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
