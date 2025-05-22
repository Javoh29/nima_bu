from typing import List, Union, Optional
from pydantic import BaseModel


class MainItemSchema(BaseModel):
    id: int
    url: str
    photo: str
    full_price: Optional[Union[int, float]] = None
    sell_price: Union[int, float]
    title: str


class MainSchema(BaseModel):
    service_title: str
    total: int
    offset: int
    limit: int
    items: List[MainItemSchema]
