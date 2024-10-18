from fastapi import APIRouter, status

from configs.settings import settings

router = APIRouter(tags=["Health Checks"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok", "version": settings.VERSION}


@router.get("/readiness", status_code=status.HTTP_200_OK)
async def readiness_check():
    return {"status": "ok", "version": settings.VERSION}
