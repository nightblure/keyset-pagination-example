from datetime import datetime, timedelta
from multiprocessing.pool import Pool
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import User


class UsersDAO:
    model = User

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_offset_items(
            self,
            *,
            offset: int,
            page_size: int,
    ) -> list[User]:
        stmt = (
            select(self.model)
            .order_by(self.model.created_at.desc())
            .limit(page_size)
            .offset(offset)
        )
        items = self.db_session.execute(stmt).scalars().all()
        return items

    def get_keyset_items(
            self,
            *,
            page_size: int,
            last_item_sorting_value: Any,
    ) -> list[User]:
        filters = []

        if last_item_sorting_value is not None:
            keyset_filter = self.model.created_at < last_item_sorting_value
            filters.append(keyset_filter)

        stmt = (
            select(self.model)
            .where(*filters)
            .order_by(self.model.created_at.desc())
            .limit(page_size)
        )
        items = self.db_session.execute(stmt).scalars().all()
        return items

    def generate_users(self, *, count: int, concurrency: int) -> None:
        start_date = datetime.today()
        batch_size = count // concurrency

        task_args = [
            (
                batch_size,
                start_date - timedelta(minutes=(i + 1) * batch_size)
            )
            for i in range(concurrency)
        ]

        from src.users_generator import generate_users

        with Pool(processes=concurrency) as pool:
            results = pool.starmap(generate_users, task_args)

        for raw_users in results:
            # stmt = insert(User).values(raw_users)
            # self.db_session.execute(stmt)
            self.db_session.bulk_insert_mappings(mapper=User, mappings=raw_users)

        self.db_session.commit()
