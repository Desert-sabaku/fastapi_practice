from typing import Optional

from pydantic import BaseModel


class ItemPayload(BaseModel):
    id: Optional[int] = None
    name: str
    quantity: int
