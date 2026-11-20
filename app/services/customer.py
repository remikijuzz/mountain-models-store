from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import BusinessRuleError, DuplicateEntityError, EntityNotFoundError
from app.models import Customer
from app.repositories import customers, orders
from app.schemas.customer import CustomerWrite


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Customer]:
        return customers.list_all(self.db)

    def get(self, customer_id: int, *, lock: bool = False) -> Customer:
        customer = customers.get_by_id(self.db, customer_id, lock=lock)
        if customer is None:
            raise EntityNotFoundError(f"Klient o ID {customer_id} nie istnieje.")
        return customer

    def create(self, data: CustomerWrite) -> Customer:
        customer = Customer(name=data.name, email=data.email.lower())
        try:
            with self.db.begin():
                customers.add(self.db, customer)
        except IntegrityError as exc:
            if exc.orig.diag.constraint_name == "uq_customers_email":
                raise DuplicateEntityError("Klient z tym adresem e-mail już istnieje.") from exc
            raise
        return customer

    def update(self, customer_id: int, data: CustomerWrite) -> Customer:
        try:
            with self.db.begin():
                customer = self.get(customer_id, lock=True)
                customer.name = data.name
                customer.email = data.email.lower()
        except IntegrityError as exc:
            if exc.orig.diag.constraint_name == "uq_customers_email":
                raise DuplicateEntityError("Klient z tym adresem e-mail już istnieje.") from exc
            raise
        return customer

    def delete(self, customer_id: int) -> None:
        with self.db.begin():
            customer = self.get(customer_id, lock=True)
            if orders.exists_for_customer(self.db, customer_id):
                raise BusinessRuleError("Klient ma powiązane zamówienia i nie można go usunąć.")
            customers.delete(self.db, customer)
