import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import api

app = FastAPI()

app.include_router(api.llmbackendRouter)
app.include_router(api.promptRouter)
app.include_router(api.automcRouter)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"]
)

@app.get("/")
def hello_world():
        return "hello world!"

if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=18000)