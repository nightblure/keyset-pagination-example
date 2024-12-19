from datetime import datetime, timedelta

from faker import Faker

from src.di import di_container
from src.models import User

fake = Faker()

def generate_users(size: int, start_date: datetime):
    raw_users = []
    # session = di_container.db_session.instance

    for i in range(size):
        raw_user = {
            "email": fake.email(),
            "username": fake.user_name(),
            "created_at": start_date - timedelta(minutes=i + 1),
        }
        raw_users.append(raw_user)

        # if i > 0 and i % percent_count == 0:
    # session.bulk_insert_mappings(mapper=User, mappings=raw_users)
    return raw_users
    # raw_users.clear()
    # print(f"Progress: {i // percent_count}%")
