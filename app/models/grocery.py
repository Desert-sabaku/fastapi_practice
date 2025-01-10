from pydantic import BaseModel


class ItemPayload(BaseModel):
    id: int | None = None
    name: str
    quantity: int
