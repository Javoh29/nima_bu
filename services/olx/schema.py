from typing import List, Optional
from services.main.schema import MainSchema, MainItemSchema
from pydantic import BaseModel, field_validator, Field, AliasPath


class PhotoSchema(BaseModel):
    link: str
    height: int
    width: int


class PriceSchema(BaseModel):
    value: Optional[int] = None
    previous_value: Optional[float] = None
    converted_value: Optional[float] = None
    converted_previous_value: Optional[float] = None
    converted_currency: Optional[str] = None


class ParamSchema(BaseModel):
    key: str
    name: str
    value: Optional[PriceSchema] = None


class ItemSchema(BaseModel):
    id: int
    photo: Optional[str] = Field(validation_alias=AliasPath('photos'))
    title: str
    url: str
    # params: List[ParamSchema]
    price: float = Field(validation_alias=AliasPath('params', ))

    @field_validator("price", mode="before")
    @classmethod
    def extract_price_param(cls, params):
        for param in params:
            if param.get("key") == "price" and isinstance(param.get("value"), dict):
                price: PriceSchema = PriceSchema(**param["value"])
                return price.converted_value or price.value
        return 0
    
    @field_validator("photo", mode="before")
    @classmethod
    def extract_photos_link(cls, photos):
        if photos:
            photo = PhotoSchema.model_validate(photos[0])
            return photo.link.format(height=photo.height, width=photo.width)
        return None
        


class Metadata(BaseModel):
    total_elements: int
    visible_total_count: int



class ClientCompatibleListings(BaseModel):
    items: List[ItemSchema]
    total: Optional[int] = Field(validation_alias=AliasPath("metadata", "total_elements"))


class DataSchema(BaseModel):
    clientCompatibleListings: ClientCompatibleListings


class OlxSearchSchema(BaseModel):
    data: DataSchema

    def to_main_schema(self, offset=0, limit=3):
        data = self.data.clientCompatibleListings
        items = [MainItemSchema(id=item.id, photo=item.photo, title=item.title, sell_price=item.price, url=item.url) for item in data.items]
        return MainSchema(service_title="OLX", total=data.total, items=items, offset=offset, limit=limit)