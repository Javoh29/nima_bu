from typing import List, Optional
from pydantic import BaseModel, field_validator, Field, AliasPath
# from services.main.schema import MainSchema, ItemSchema as MainItemSchema
from typing import List, Union, Optional
from pydantic import BaseModel

from services.main.schema import MainItemSchema, MainSchema





class CatalogCardSchema(BaseModel):
    minFullPrice: int
    minSellPrice: int
    id: int
    title: str
    photo: Optional[str] = Field(validation_alias=AliasPath("photos", 0, "link", "high"))

class ItemSchema(BaseModel):
    catalogCard: CatalogCardSchema


class MakeSearchSchema(BaseModel):
    total: int
    items: List[ItemSchema]


class DataSchema(BaseModel):
    makeSearch: MakeSearchSchema


class UzumSearchSchema(BaseModel):
    data: DataSchema

    def to_main_schema(self, offset: int = 0, limit : int = 3) -> MainSchema:
        data = self.data.makeSearch
        items = [
            MainItemSchema(
                id=(catalog_card:=item.catalogCard).id, 
                photo=catalog_card.photo, 
                title=catalog_card.title,
                full_price=catalog_card.minFullPrice, 
                sell_price=catalog_card.minSellPrice, 
                url="https://uzum.uz/uz/product/{id}?utm_source=sharing&utm_medium=product_page_android&utm_campaign=native".format(id=catalog_card.id)
            ) for item in data.items
        ]
        main_schema = MainSchema(service_title="Uzum Market", total=data.total, items=items, offset=offset, limit=limit)
        return main_schema
