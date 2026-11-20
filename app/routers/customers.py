from fastapi import APIRouter, Response, status

from app.routers import DbSession
from app.schemas.customer import CustomerRead, CustomerWrite
from app.services.customer import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=list[CustomerRead])
def list_customers(db: DbSession):
    return CustomerService(db).list_all()


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: DbSession):
    return CustomerService(db).get(customer_id)


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerWrite, db: DbSession):
    return CustomerService(db).create(data)


@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, data: CustomerWrite, db: DbSession):
    return CustomerService(db).update(customer_id, data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_customer(customer_id: int, db: DbSession) -> None:
    CustomerService(db).delete(customer_id)
