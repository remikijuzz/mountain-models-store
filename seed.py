from decimal import Decimal

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Customer, MountainModel


def seed() -> None:
    Base.metadata.create_all(bind=engine)

    customers = [
        Customer(name="Anna Kowalska", email="anna@example.com"),
        Customer(name="Jan Nowak", email="jan@example.com"),
    ]
    models = [
        MountainModel(
            name="Tatry", mountain_range="Tatry", scale="1:50000",
            price=Decimal("149.90"), stock_quantity=10,
        ),
        MountainModel(
            name="Bieszczady", mountain_range="Bieszczady", scale="1:75000",
            price=Decimal("99.90"), stock_quantity=5,
        ),
        MountainModel(
            name="Karkonosze", mountain_range="Karkonosze", scale="1:50000",
            price=Decimal("119.90"), stock_quantity=0, is_active=False,
        ),
    ]

    with SessionLocal.begin() as db:
        existing_emails = set(db.scalars(select(Customer.email)))
        existing_model_names = set(db.scalars(select(MountainModel.name)))
        db.add_all(customer for customer in customers if customer.email not in existing_emails)
        db.add_all(model for model in models if model.name not in existing_model_names)

    print("Dane demonstracyjne są gotowe.")


if __name__ == "__main__":
    seed()
