from sqlmodel import create_engine, text,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config
from src.db.model import Book

engine = AsyncEngine(create_engine(
   Config.DATABASE_URL,
   echo=True
))
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async_session_maker=sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session():
    async with async_session_maker() as session:
        yield session