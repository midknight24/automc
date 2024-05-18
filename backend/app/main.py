import uvicorn
from fastapi import FastAPI

from . import api

app = FastAPI()

app.include_router(api.llmbackendRouter)
app.include_router(api.promptRouter)
app.include_router(api.automcRouter)


@app.get("/")
def hello_world():
        return "hello world!"

if __name__ == "__main__":
        uvicorn.run(app)