from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Customer


def list_all(db: Session) -> list[Customer]:
    return list(db.scalars(select(Customer).order_by(Customer.id)))


def get_by_id(db: Session, customer_id: int, *, lock: bool = False) -> Customer | None:
    return db.get(Customer, customer_id, with_for_update=True if lock else None)


def add(db: Session, customer: Customer) -> None:
    db.add(customer)


def delete(db: Session, customer: Customer) -> None:
    db.delete(customer)
