from . import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException, status

async def get_sensor_records(db: AsyncSession, limit: int, page: int, sensor_model: str):
    skip = (page - 1) * limit
    query = select(models.SensorRecord).filter(
        models.SensorRecord.sensor_model.contains(sensor_model)
    ).limit(limit).offset(skip)
    result = await db.execute(query)
    sensor_records = result.scalars().all()
    return {'results': len(sensor_records), 'records': sensor_records}

async def create_sensor_record(db: AsyncSession, payload: schemas.SensorRecordCreateDTO):
    new_sensor_record = models.SensorRecord(**payload.dict())
    db.add(new_sensor_record)
    await db.commit()
    await db.refresh(new_sensor_record)
    return {'sensor_record': new_sensor_record}

async def update_sensor_record(db: AsyncSession, sensorId: str, payload: schemas.SensorRecordBaseSchema):
    query = select(models.SensorRecord).filter(models.SensorRecord.id == sensorId)
    result = await db.execute(query)
    db_sensor_record = result.scalar_one_or_none()
    
    if not db_sensor_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f'Nenhum sensor com o ID: {sensorId} encontrado')
    
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sensor_record, key, value)
    
    await db.commit()
    await db.refresh(db_sensor_record)
    return {'sensor_record': db_sensor_record}

async def get_sensor_record(db: AsyncSession, sensorId: str):
    query = select(models.SensorRecord).filter(models.SensorRecord.id == sensorId)
    result = await db.execute(query)
    sensor_record = result.scalar_one_or_none()
    
    if not sensor_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f'Nenhum sensor com o ID: {sensorId} encontrado')
    return {'sensor_record': sensor_record}

async def delete_sensor_record(db: AsyncSession, sensorId: str):
    query = select(models.SensorRecord).filter(models.SensorRecord.id == sensorId)
    result = await db.execute(query)
    sensor_record = result.scalar_one_or_none()
    
    if not sensor_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f'Nenhum sensor com o ID: {sensorId} encontrado')
    
    await db.delete(sensor_record)
    await db.commit()
    return None