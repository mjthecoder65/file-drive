from fastapi import FastAPI

from configs.settings import settings
from routers import auth, files, insights, users, health_checks

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.debug,
    docs_url="/",
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(files.router)
app.include_router(insights.router)
app.include_router(health_checks.router)
