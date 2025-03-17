from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

engine = create_async_engine(
    "sqlite+aiosqlite:///./note.db", echo=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


@asynccontextmanager
async def get_db_session():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_db():
    async with get_db_session() as db:
        yield db
