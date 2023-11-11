from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from routers.articles_router import router as router_article
from routers.pages_router import router as router_page
from routers.systems_router import router as router_system
from routers.chats_router import router as router_chat
from routers.user_router import router as router_user
from routers.auth_router import router as router_auth
from routers.database_router import router as router_db
from routers.queries_router import router as router_query

app = FastAPI(
    title="Smart Search"
)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_system)
app.include_router(router_chat)
app.include_router(router_article)
app.include_router(router_query)
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
