from ..core.database import Base
from sqlalchemy import TIMESTAMP, Column, String, Float
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE


class SensorRecord(Base):
    __tablename__ = 'sensor_record'
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    sensor_model = Column(String, nullable=False)
    measure_unit = Column(String, nullable=False)
    location = Column(String, nullable=False, index=True)
    data_type = Column(String, nullable=False)
    data = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())
