from . import service, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, APIRouter, Response
from ..core.database import get_db

router = APIRouter(tags=['Sensor'])

@router.get('')
async def get_sensor_records(db: AsyncSession = Depends(get_db), limit: int = 10, page: int = 1, sensor_model: str = ''):
    return await service.get_sensor_records(db, limit, page, sensor_model)

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_sensor_record(payload: schemas.SensorRecordCreateDTO, db: AsyncSession = Depends(get_db)):
    return await service.create_sensor_record(db, payload)

@router.patch('/{sensorId}')
async def update_sensor_record(sensorId: str, payload: schemas.SensorRecordBaseSchema, db: AsyncSession = Depends(get_db)):
    return await service.update_sensor_record(db, sensorId, payload)

@router.get('/{sensorId}')
async def get_sensor_record(sensorId: str, db: AsyncSession = Depends(get_db)):
    return await service.get_sensor_record(db, sensorId)

@router.delete('/{sensorId}')
async def delete_sensor_record(sensorId: str, db: AsyncSession = Depends(get_db)):
    await service.delete_sensor_record(db, sensorId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
