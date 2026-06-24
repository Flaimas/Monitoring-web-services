from pydantic import BaseModel, ConfigDict
from pydantic.networks import HttpUrl

class UrlCreateSchema(BaseModel):
    url: HttpUrl
    title: str

class UrlResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    title: str
    is_active: bool