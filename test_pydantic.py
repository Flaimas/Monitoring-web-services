from pydantic import BaseModel, ValidationError, Field, EmailStr, field_validator, model_validator

class City(BaseModel):
    city_id: int
    name: str = Field(alias='cityFullName')

    @model_validator(mode='after')
    def name_should_be_spb(self) -> str:
        print("values", self.city_id, self.name)
        return self

imput_json = """{
    "city_id": "123",
    "cityFullName": "spb",
    "svo": "dadadada"
 }"""

try:
    city = City.model_validate_json(imput_json)
    print(city)
    print(city.model_dump_json(by_alias=True,
                               exclude={"city_id"}))

except ValidationError as e:
    print(e.json(indent=4))