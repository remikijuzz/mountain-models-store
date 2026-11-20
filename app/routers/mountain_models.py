from fastapi import APIRouter, Response, status

from app.routers import DbSession
from app.schemas.mountain_model import MountainModelRead, MountainModelWrite
from app.services.mountain_model import MountainModelService

router = APIRouter(prefix="/models", tags=["Mountain Models"])


@router.get("", response_model=list[MountainModelRead])
def list_models(db: DbSession):
    return MountainModelService(db).list_all()


@router.get("/{model_id}", response_model=MountainModelRead)
def get_model(model_id: int, db: DbSession):
    return MountainModelService(db).get(model_id)


@router.post("", response_model=MountainModelRead, status_code=status.HTTP_201_CREATED)
def create_model(data: MountainModelWrite, db: DbSession):
    return MountainModelService(db).create(data)


@router.put("/{model_id}", response_model=MountainModelRead)
def update_model(model_id: int, data: MountainModelWrite, db: DbSession):
    return MountainModelService(db).update(model_id, data)


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_model(model_id: int, db: DbSession) -> None:
    MountainModelService(db).delete(model_id)
