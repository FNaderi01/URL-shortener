import secrets
import string

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models


def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


async def create_unique_key(db: AsyncSession) -> str:
    key = create_random_key()
    while await key_exists(db, key):
        key = create_random_key()
    return key


async def key_exists(db: AsyncSession, key: str) -> bool:
    result = await db.execute(select(models.URL.id).where(models.URL.key == key))
    return result.scalar_one_or_none() is not None
