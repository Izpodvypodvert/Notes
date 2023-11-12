from fastapi import FastAPI
from routers.note_router import router as note_router
from routers.user_router import router as user_router


app = FastAPI()

app.include_router(note_router, prefix="/notes", tags=["Notes"])
app.include_router(user_router)
