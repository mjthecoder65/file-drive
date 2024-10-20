from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str


class ReadinessCheckResponse(HealthCheckResponse):
    pass
