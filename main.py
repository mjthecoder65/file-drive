import uvicorn
from fastapi import FastAPI

from configs.settings import settings
from routers import auth, files, insights, users

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.debug,
    docs_url="/",
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
