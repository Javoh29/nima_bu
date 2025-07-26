from typing import List, Optional, Union
from pydantic import BaseModel, Field, AliasPath
from services.main.schema import MainItemSchema, MainSchema

class Price(BaseModel):
    basic: int
    product: int


class Size(BaseModel):
    price: Price


class ItemSchema(BaseModel):
    id: int
    name: str
    brand: str
    full_price: int = Field(validation_alias=AliasPath("sizes", 0, "price", "basic"))
    sell_price: int = Field(validation_alias=AliasPath("sizes", 0, "price", "product"))


class DataSchema(BaseModel):
    products: List[ItemSchema]
    total: int


class WildberriesSearchSchema(BaseModel):
    data: DataSchema

    def to_main_schema(self, offset: int = 0, limit: int = 3):
        items = [
            MainItemSchema(
                id=(product_id:=product.id),
                url=f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx",
                photo=f"https://alm-basket-cdn-01.geobasket.ru/vol{str(product_id)[:-5]}/part{str(product_id)[:-3]}/{product_id}/images/big/1.webp",
                full_price=product.full_price,
                sell_price=product.sell_price,
                title=("%s %s" % (product.brand, product.name)).strip()
            )
            for product in self.data.products
        ]

        return MainSchema(
            service_title="WildBerries",
            total=self.data.total,
            offset=offset,
            limit=limit,
            items=items
        )


