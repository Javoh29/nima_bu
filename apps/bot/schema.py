from pydantic import BaseModel


class TextShowMoreSchema(BaseModel):
    text: str
    offset: int
    service_title: str


class ImageShowMoreSchema(BaseModel):
    image_path: str
    offset: int
    service_title: str