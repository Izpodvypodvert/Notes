from fastapi import Depends, FastAPI

from dependencies.redis import redis_lifespan
from routers.note_router import router as note_router
from routers.category_router import router as category_router
from routers.user_router import router as user_router


app = FastAPI(lifespan=redis_lifespan)

app.include_router(note_router, prefix="/notes", tags=["Notes"])
app.include_router(category_router, prefix="/categories", tags=["Categories"])
app.include_router(user_router)
