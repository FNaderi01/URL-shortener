from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import keygen, models, schemas


async def get_db_url_by_key(db: AsyncSession, key: str) -> models.URL | None:
    result = await db.execute(
        select(models.URL).where(
            models.URL.key == key,
            models.URL.is_active.is_(True),
        )
    )
    return result.scalar_one_or_none()


async def get_db_url_by_secret_key(db: AsyncSession, secret_key: str) -> models.URL | None:
    result = await db.execute(
        select(models.URL).where(
            models.URL.secret_key == secret_key,
            models.URL.is_active.is_(True),
        )
    )
    return result.scalar_one_or_none()


async def create_db_url(db: AsyncSession, url: schemas.URLBase) -> models.URL:
    key = await keygen.create_unique_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"

    db_url = models.URL(
        target_url=url.target_url,
        key=key,
        secret_key=secret_key,
        is_active=True,
        clicks=0,
    )
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return db_url


async def update_clicks(db: AsyncSession, db_url: models.URL) -> None:
    db_url.clicks += 1
    await db.commit()


async def delete_db_url(db: AsyncSession, db_url: models.URL) -> None:
    db_url.is_active = False
    await db.commit()
