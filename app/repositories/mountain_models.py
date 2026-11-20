from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import MountainModel


def list_all(db: Session) -> list[MountainModel]:
    return list(db.scalars(select(MountainModel).order_by(MountainModel.id)))


def get_by_id(db: Session, model_id: int, *, lock: bool = False) -> MountainModel | None:
    return db.get(MountainModel, model_id, with_for_update=True if lock else None)


def add(db: Session, model: MountainModel) -> None:
    db.add(model)


def delete(db: Session, model: MountainModel) -> None:
    db.delete(model)
