from fastapi import FastAPI

from routers.apiForm import router as form_router
from routers.apiJson import router as json_router

app = FastAPI()
app.include_router(form_router)
app.include_router(json_router, prefix="/user")

@app.get("/")
async def root():
    return {"message": "Hello World"}
