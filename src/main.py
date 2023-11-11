from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from routers.articles_router import router as router_article
from routers.pages_router import router as router_page
from routers.database_router import router as router_db

app = FastAPI(
    title="Smart Search"
)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(router_article)
app.include_router(router_db)
app.include_router(router_page)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
