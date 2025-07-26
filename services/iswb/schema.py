from pydantic import BaseModel, field_validator, Field, AliasPath
from typing import List, Optional, Any
from services.main.schema import MainItemSchema, MainSchema

class PredictionSchema(BaseModel):
    bbox: List[float]
    label_id: int
    label: str
    label_ru: str
    confidence: float

class CategoryDetectionSchema(BaseModel):
    predictions: List[PredictionSchema]
    predictions_ocr: List = []
    engine: str
    error_ocr: Optional[str]


class ItemSchema(BaseModel):
    id: int
    name: str
    brand: str
    full_price: int = Field(validation_alias=AliasPath("sizes", 0, "price", "basic"))
    sell_price: int = Field(validation_alias=AliasPath("sizes", 0, "price", "product"))



class DataSchema(BaseModel):
    products: List[ItemSchema]


class CatalogSchema(BaseModel):
    data: DataSchema


class ISWBSchema(BaseModel):
    catalog: CatalogSchema

    def to_main_schema(self, offset: int = 0, limit: int = 3):
        products = self.catalog.data.products
        total = len(products)
        items = []
        for index, product in enumerate(products):
            if offset <= index < offset+limit:
                product_id = product.id
                item = MainItemSchema(
                    id=product_id,
                    url=f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx",
                    photo=f"https://alm-basket-cdn-01.geobasket.ru/vol{str(product_id)[:-5]}/part{str(product_id)[:-3]}/{product_id}/images/big/1.webp",
                    full_price=product.full_price,
                    sell_price=product.sell_price,
                    title=("%s %s" % (product.brand, product.name)).strip()
                )
                items.append(item)

        return MainSchema(
            service_title="WildBerries",
            total=total,
            offset=offset,
            limit=limit,
            items=items
        )
