from pydantic import BaseModel, ConfigDict


class VINSchema(BaseModel):
    id: int
    version: str
    equipment_code: str
    year_of_issue: str
    serial_number: int
    place_of_production: str
    model_config = ConfigDict(from_attributes=True)


class VINAddRequest(BaseModel):
    version: str
    equipment_code: str
    year_of_issue: str
    serial_number: int
    place_of_production: str


class VINSearchRequest(BaseModel):
    version: str
    equipment_code: str
    year_of_issue: str
    place_of_production: str


class VINSearchResponse(BaseModel):
    next_serial_number: int
