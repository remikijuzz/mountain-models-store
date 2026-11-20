from sqlalchemy.orm import Session

from app.exceptions import BusinessRuleError, EntityNotFoundError
from app.models import MountainModel
from app.repositories import mountain_models, orders
from app.schemas.mountain_model import MountainModelWrite


class MountainModelService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[MountainModel]:
        return mountain_models.list_all(self.db)

    def get(self, model_id: int, *, lock: bool = False) -> MountainModel:
        model = mountain_models.get_by_id(self.db, model_id, lock=lock)
        if model is None:
            raise EntityNotFoundError(f"Makieta o ID {model_id} nie istnieje.")
        return model

    def create(self, data: MountainModelWrite) -> MountainModel:
        model = MountainModel(**data.model_dump())
        with self.db.begin():
            mountain_models.add(self.db, model)
        return model

    def update(self, model_id: int, data: MountainModelWrite) -> MountainModel:
        with self.db.begin():
            model = self.get(model_id, lock=True)
            model.name = data.name
            model.mountain_range = data.mountain_range
            model.scale = data.scale
            model.price = data.price
            model.stock_quantity = data.stock_quantity
            model.is_active = data.is_active
        return model

    def delete(self, model_id: int) -> None:
        with self.db.begin():
            model = self.get(model_id, lock=True)
            if orders.exists_for_model(self.db, model_id):
                raise BusinessRuleError("Makieta ma powiązane zamówienia i nie można jej usunąć.")
            mountain_models.delete(self.db, model)
