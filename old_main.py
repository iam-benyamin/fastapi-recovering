
from typing import Annotated

from fastapi import Body, Depends, FastAPI
from pydantic import BaseModel


class CreatePostIn(BaseModel):
    title: str
    content: str


app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/blogs/")
async def blog_list(param: Annotated[dict, Depends(common_parameters)]):
    return {"result": [1, 2, 3, 4, 5]}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# is_private is query parameter
@app.get("/blog/{slog}/")
async def blog(slog: str, is_private: bool = False):
    return {"message": f"slog {slog}, is_private: {is_private}"}


@app.post("/blog/create")
async def create_post(post: CreatePostIn = Body()):
    return post


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app)
