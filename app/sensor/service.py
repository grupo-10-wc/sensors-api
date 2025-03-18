import datetime
import numpy as np
from . import models, schemas
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
import matplotlib.pyplot as plt



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
    return {'record': new_sensor_record}

async def create_sensor_records_bulk(db: AsyncSession, payloads: list[schemas.SensorRecordCreateDTO]):
    new_sensor_records = [models.SensorRecord(**payload.dict()) for payload in payloads]
    db.add_all(new_sensor_records)
    await db.commit()
    
    return {'status': "success"}

async def get_sensor_record(db: AsyncSession, sensorId: str):
    query = select(models.SensorRecord).filter(models.SensorRecord.id == sensorId)
    result = await db.execute(query)
    sensor_record = result.scalar_one_or_none()
    
    if not sensor_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f'Nenhum sensor com o ID: {sensorId} encontrado')
    return {'record': sensor_record}

async def update_sensor_record(db: AsyncSession, sensorId: str, payload: schemas.SensorRecordUpdateDTO):
    result = await get_sensor_record(db, sensorId)
    sensor_record = result['record']

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sensor_record, key, value)
    
    await db.commit()
    await db.refresh(sensor_record)
    return {'record': sensor_record}

async def delete_sensor_record(db: AsyncSession, sensorId: str):
    result = await get_sensor_record(db, sensorId)
    sensor_record = result['record']
    await db.delete(sensor_record)
    await db.commit()
    return None

async def mock_fluke1735(db: AsyncSession, n_days: int):
    def calcular_fator_potencia(tensao, corrente, angulo_fase):
        angulo_fase_rad = np.radians(angulo_fase)
        
        potencia_ativa = tensao * corrente * np.cos(angulo_fase_rad)
        potencia_aparente = tensao * corrente
        fator_potencia = potencia_ativa / potencia_aparente
        
        return fator_potencia

    n_amostras = n_days * 24 * 60  # 1 amostra por minuto

    np.random.seed(1337)

    # Criar variações suaves com componente aleatório
    ruido_tensao = np.random.normal(0, 1, n_amostras)
    ruido_corrente = np.random.normal(0, 0.5, n_amostras)

    # Aplicar filtro de média móvel para suavizar o ruído
    window = int(n_amostras / 10 / 2)
    ruido_tensao = np.convolve(ruido_tensao, np.ones(window)/window, mode='same')
    ruido_corrente = np.convolve(ruido_corrente, np.ones(window)/window, mode='same')

    tensoes = 220 + ruido_tensao * 5  # Tensão base + ruído suavizado
    correntes = 10 + ruido_corrente * 2  # Corrente base + ruído suavizado

    # Gerar ângulo de fase com variações aleatórias
    angulo_base = 23.07  # Equivalente a FP = 0.92
    ruido_angulo = np.random.normal(0, 40, n_amostras)
    ruido_angulo = np.convolve(ruido_angulo, np.ones(window)/window, mode='same')
    angulos_fase = angulo_base + ruido_angulo

    fatores_potencia = [round(float(calcular_fator_potencia(V, I, ang)), 5) 
                       for V, I, ang in zip(tensoes, correntes, angulos_fase)]
    payload = []
    start_date = datetime.datetime.now()    
    

    for i in range(len(fatores_potencia)):
        record = schemas.SensorRecordCreateDTO(
            sensor_model='Fluke 1735',
            measure_unit='kW',
            device='Ar Condicionado',
            location='Sala de reuniões',
            data_type='Fator de Potência',
            data=fatores_potencia[i],
            created_at=start_date + datetime.timedelta(minutes=i)
        )
        payload.append(record)
    return await create_sensor_records_bulk(db, payload)

async def mock_shelly_sensor(db: AsyncSession, n_days: int):
    np.random.seed(1337)
    n_amostras = n_days * 24 * 60  
    
    ruido_consumo = np.random.normal(0, 0.05, n_amostras)
    window = int(n_amostras / 10 / 2)
    ruido_consumo = np.convolve(ruido_consumo, np.ones(window)/window, mode='same')
    consumos = 1 + ruido_consumo
    
    payload = []
    start_date = datetime.datetime.now()
    
    for i in range(len(consumos)):
        record = schemas.SensorRecordCreateDTO(
            sensor_model='Shelly EM',
            measure_unit='kWh',
            device='Disjuntor Geral',
            location='Quadro de Energia',
            data_type='Consumo de Energia',
            data=round(float(consumos[i]), 5),
            created_at=start_date + datetime.timedelta(minutes=i)
        )
        payload.append(record)
    
    return await create_sensor_records_bulk(db, payload)
async def mock_pzem004t(db: AsyncSession, n_minutes: int, threshold: float = 5.0):
    n_samples = n_minutes * 60 * 10  # 10 samples per second

    np.random.seed(42)

    # Generate smooth voltage variations with random noise
    base_voltage = 220
    noise = np.random.normal(0, 1, n_samples)
    voltage_readings = base_voltage + noise

    # Detect voltage oscillations
    oscillations = []
    for i in range(1, len(voltage_readings)):
        if abs(voltage_readings[i] - voltage_readings[i - 1]) > threshold:
            oscillations.append((i, voltage_readings[i]))

    # Store readings in the database
    payload = []
    start_time = datetime.datetime.now()
    for i, voltage in enumerate(voltage_readings):
        record = schemas.SensorRecordCreateDTO(
            sensor_model='PZEM-004T',
            measure_unit='V',
            device='Rede Elétrica',
            location='Instalação',
            data_type='Tensão',
            data=voltage,
            created_at=start_time + datetime.timedelta(seconds=i / 10)
        )
        payload.append(record)
    await create_sensor_records_bulk(db, payload)

    # Plot voltage readings
    times = [start_time + datetime.timedelta(seconds=i / 10) for i in range(len(voltage_readings))]
    plt.figure(figsize=(10, 5))
    plt.plot(times, voltage_readings, label='Tensão (V)')
    for osc in oscillations:
        plt.axvline(x=times[osc[0]], color='r', linestyle='--', label='Oscilação' if osc == oscillations[0] else "")
    plt.xlabel('Tempo')
    plt.ylabel('Tensão (V)')
    plt.title('Leituras de Tensão Simuladas e Oscilações Detectadas')
    plt.legend()
    plt.grid(True)
    plt.savefig('voltage_oscillations.png')

    return {'status': 'success', 'oscillations': len(oscillations)}
