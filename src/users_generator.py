from datetime import datetime, timedelta

from faker import Faker

fake = Faker()

def generate_users(size: int, start_date: datetime):
    raw_users = []

    for i in range(size):
        raw_user = {
            "email": fake.email(),
            "username": fake.user_name(),
            "created_at": start_date - timedelta(minutes=i + 1),
        }
        raw_users.append(raw_user)

    return raw_users
