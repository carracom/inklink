import uvicorn
from fastapi import FastAPI

from routes.book import router as books_router
from routes.author import router as authors_router
from routes.publisher import router as publisher_router
from routes.users import router as users_router
from controllers.users import create_user, login
from models.login import Login
from models.users import User

app = FastAPI(title="InkLink API", version="2.0")

app.include_router(books_router, prefix="/books", tags=["books"])

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="InkLink API", version="2.0") 


@app.post("/users", response_model=User)
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)


@app.post("/login")
async def login_access(l: Login) -> dict:
    return await login(l)


app.include_router(authors_router, prefix="/authors", tags=["authors"])
app.include_router(publisher_router, prefix="/publishers", tags=["publishers"])
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(users_router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

    from fastapi import FastAPI


app = FastAPI(title="InkLink API", version="2.0")


