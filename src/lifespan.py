from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from src.di import di_container
from src.models import Base


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    di_container.postgres_container()
    Base.metadata.create_all(bind=di_container.sqla_engine())

    await di_container.init_all_resources()

    users_dao = di_container.users_dao()

    multiple = 2
    users_dao.generate_users(count=multiple * (10 ** 6), concurrency=10)

    try:
        yield
    finally:
        await di_container.close_all_resources()
