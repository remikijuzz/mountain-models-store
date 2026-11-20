from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.exceptions import BusinessRuleError, EntityNotFoundError
from app.models import Order
from app.order_status import OrderStatus
from app.repositories import customers, mountain_models, orders
from app.schemas.order import OrderCreate

NEXT_STATUS = {
    OrderStatus.NEW: OrderStatus.PAID,
    OrderStatus.PAID: OrderStatus.SHIPPED,
}


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Order]:
        return orders.list_all(self.db)

    def get(self, order_id: int, *, lock: bool = False) -> Order:
        order = orders.get_by_id(self.db, order_id, lock=lock)
        if order is None:
            raise EntityNotFoundError(f"Zamówienie o ID {order_id} nie istnieje.")
        return order

    def create(self, data: OrderCreate) -> Order:
        with self.db.begin():
            customer = customers.get_by_id(self.db, data.customer_id, lock=True)
            if customer is None:
                raise EntityNotFoundError(f"Klient o ID {data.customer_id} nie istnieje.")

            # Blokada makiety obejmuje sprawdzenie stanu i odjęcie sztuk.
            model = mountain_models.get_by_id(self.db, data.mountain_model_id, lock=True)
            if model is None:
                raise EntityNotFoundError(f"Makieta o ID {data.mountain_model_id} nie istnieje.")
            if not model.is_active:
                raise BusinessRuleError("Makieta jest nieaktywna.")
            if model.stock_quantity < data.quantity:
                raise BusinessRuleError(
                    f"Za mało sztuk w magazynie. Dostępne: {model.stock_quantity}, "
                    f"zamówione: {data.quantity}."
                )

            discount_percent = 10 if data.quantity >= 3 else 0
            subtotal = model.price * data.quantity
            total = (subtotal * (100 - discount_percent) / 100).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            if total > Decimal("99999999.99"):
                raise BusinessRuleError("Łączna cena przekracza limit 99 999 999,99.")

            model.stock_quantity -= data.quantity
            order = Order(
                customer_id=customer.id,
                mountain_model_id=model.id,
                quantity=data.quantity,
                unit_price=model.price,
                discount_percent=discount_percent,
                total_price=total,
            )
            orders.add(self.db, order)
        return order

    def change_status(self, order_id: int, new_status: OrderStatus) -> Order:
        with self.db.begin():
            order = self.get(order_id, lock=True)
            if NEXT_STATUS.get(order.status) != new_status:
                raise BusinessRuleError(
                    f"Niedozwolona zmiana statusu z {order.status.value} na {new_status.value}."
                )
            order.status = new_status
        return order

    def cancel(self, order_id: int) -> Order:
        with self.db.begin():
            order = self.get(order_id, lock=True)
            if order.status in (OrderStatus.SHIPPED, OrderStatus.CANCELLED):
                raise BusinessRuleError(
                    f"Nie można anulować zamówienia o statusie {order.status.value}."
                )

            model = mountain_models.get_by_id(self.db, order.mountain_model_id, lock=True)
            if model is None:
                raise EntityNotFoundError(f"Makieta o ID {order.mountain_model_id} nie istnieje.")
            restored_stock = model.stock_quantity + order.quantity
            if restored_stock > 2_147_483_647:
                raise BusinessRuleError("Przywrócenie sztuk przekroczyłoby limit stanu magazynu.")
            model.stock_quantity = restored_stock
            order.status = OrderStatus.CANCELLED
        return order
