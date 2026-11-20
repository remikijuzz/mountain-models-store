from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.models import Order


def list_all(db: Session) -> list[Order]:
    return list(db.scalars(select(Order).order_by(Order.id)))


def get_by_id(db: Session, order_id: int, *, lock: bool = False) -> Order | None:
    return db.get(Order, order_id, with_for_update=True if lock else None)


def add(db: Session, order: Order) -> None:
    db.add(order)


def exists_for_customer(db: Session, customer_id: int) -> bool:
    return bool(db.scalar(select(exists().where(Order.customer_id == customer_id))))


def exists_for_model(db: Session, model_id: int) -> bool:
    return bool(db.scalar(select(exists().where(Order.mountain_model_id == model_id))))
