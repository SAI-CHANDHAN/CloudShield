from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resource_id: str
    resource_type: str
    provider: str
    region: str | None = None
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
