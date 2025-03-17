from . import service, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, APIRouter, Response
from ..core.database import get_db
router = APIRouter(tags=['Sensor'])

@router.get('')
async def get_sensor_records(
    limit: int = 10,
    page: int = 1,
    sensor_model: str = '',
    db: AsyncSession = Depends(get_db)
):
    return await service.get_sensor_records(db, limit, page, sensor_model)

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_sensor_record(
    payload: schemas.SensorRecordCreateDTO,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_sensor_record(db, payload)

@router.patch('/{sensorId}')
async def update_sensor_record(
    sensorId: str,
    payload: schemas.SensorRecordUpdateDTO,
    db: AsyncSession = Depends(get_db)
):
    return await service.update_sensor_record(db, sensorId, payload)

@router.get('/{sensorId}')
async def get_sensor_record(
    sensorId: str,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_sensor_record(db, sensorId)

@router.delete('/{sensorId}')
async def delete_sensor_record(
    sensorId: str,
    db: AsyncSession = Depends(get_db)
):
    await service.delete_sensor_record(db, sensorId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/mock/fluke1735')
async def mock_fluke1735(
    days: int = 1,
    db: AsyncSession = Depends(get_db)
):
    return await service.mock_fluke1735(db, days)