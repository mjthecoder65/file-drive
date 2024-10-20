from fastapi import APIRouter, status

from schemas.health_check import HealthCheckResponse, ReadinessCheckResponse

router = APIRouter(tags=["Health Checks"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponse,
)
async def health_check():
    return {"status": "ok"}


@router.get(
    "/readiness",
    status_code=status.HTTP_200_OK,
    response_model=ReadinessCheckResponse,
)
async def readiness_check():
    return {"status": "ok"}
