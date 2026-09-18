from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.resource import Resource
from ..schemas.resource import ResourceResponse

router = APIRouter(prefix="/api/resources", tags=["resources"])


@router.get("", response_model=list[ResourceResponse])
def list_resources(db: Session = Depends(get_db)) -> list[Resource]:
    return list(db.scalars(select(Resource).order_by(Resource.id)).all())
