from fastapi import FastAPI
import uvicorn
from helpers.router import router

api = FastAPI()
api.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:api", reload=True)
