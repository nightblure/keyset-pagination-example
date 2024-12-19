from contextlib import contextmanager
from typing import Iterator, Annotated

from fastapi import Depends
from injection import DeclarativeContainer, providers, Provide
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from src.users_dao import UsersDAO as _UsersDAO


@contextmanager
def _run_postgres_container() -> Iterator[PostgresContainer]:
    container = PostgresContainer(image="postgres:14.15-alpine3.20", driver="psycopg2")
    container.start()

    try:
        yield container
    finally:
        container.stop()


def _get_db_url(container: PostgresContainer) -> str:
    return container.get_connection_url()


@contextmanager
def _db_session_resource(engine: Engine) -> Iterator[Session]:
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    try:
        yield session
    finally:
        session.close()


class DIContainer(DeclarativeContainer):
    _instance = None

    postgres_container = providers.Resource(factory=_run_postgres_container)
    db_url = providers.Factory(_get_db_url, postgres_container.cast)
    sqla_engine = providers.Factory(create_engine, url=db_url)
    db_session = providers.Resource(_db_session_resource, sqla_engine.cast, function_scope=True)
    users_dao = providers.Transient(_UsersDAO, db_session=db_session.cast)

    @classmethod
    def instance(cls) -> "DIContainer":
        if cls._instance is None:
            cls._instance = DIContainer()
        return cls._instance


di_container: DIContainer = DIContainer.instance()

UsersDAO = Annotated[_UsersDAO, Depends(Provide[di_container.users_dao])]
