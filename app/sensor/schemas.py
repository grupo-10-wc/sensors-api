from datetime import datetime
from typing import List
from pydantic import BaseModel
from uuid import UUID


class SensorRecordBaseSchema(BaseModel):
    id: UUID | None = None
    sensor_model: str
    measure_unit: str
    location: str
    data_type: str
    data: float
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class SensorRecordCreateDTO(BaseModel):
    sensor_model: str
    measure_unit: str
    location: str
    data_type: str
    data: float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        
class SensorRecordResponse(BaseModel):
    status: str
    results: int
    records: List[SensorRecordBaseSchema]
