from fastapi import APIRouter, status

from app.routers import DbSession
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from app.services.order import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("", response_model=list[OrderRead])
def list_orders(db: DbSession):
    return OrderService(db).list_all()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: DbSession):
    return OrderService(db).get(order_id)


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate, db: DbSession):
    return OrderService(db).create(data)


@router.patch("/{order_id}/status", response_model=OrderRead)
def change_order_status(order_id: int, data: OrderStatusUpdate, db: DbSession):
    return OrderService(db).change_status(order_id, data.status)


@router.post("/{order_id}/cancel", response_model=OrderRead)
def cancel_order(order_id: int, db: DbSession):
    return OrderService(db).cancel(order_id)
