from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from configs.settings import settings
from routers import auth, files, insights, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        pass


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/",
    description="""Backend API for File Drive that 
    allows users to upload and manager files.
    Service also user generative AI to enable user to issue prompt to generate insights from the uploaded files.""",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(files.router)
app.include_router(insights.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.debug,
    )
