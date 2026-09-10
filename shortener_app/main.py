import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import URL

from . import crud, models, schemas
from .config import get_settings
from .database import Base, engine, get_db

app = FastAPI()


@app.on_event("startup")
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "Administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


def raise_bad_request(message: str) -> None:
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request: Request) -> None:
    message = f"URL {request.url} Not Found!"
    raise HTTPException(status_code=404, detail=message)


@app.get("/{url_key}")
async def forward_to_target_url(
    url_key: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    if db_url := await crud.get_db_url_by_key(db, url_key):
        await crud.update_clicks(db, db_url)
        return RedirectResponse(db_url.target_url)

    raise_not_found(request)


@app.post("/url", response_model=schemas.URLInfo)
async def create_url(url: schemas.URLBase, db: AsyncSession = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    db_url = await crud.create_db_url(db=db, url=url)

    return get_admin_info(db_url)


@app.get(
    "/admin/{secret_key}",
    name="Administration info",
    response_model=schemas.URLInfo,
)
async def get_url_info(
    secret_key: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    if db_url := await crud.get_db_url_by_secret_key(db, secret_key):
        return get_admin_info(db_url)

    raise_not_found(request)


@app.delete("/admin/{secret_key}")
async def delete_url(
    secret_key: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    if db_url := await crud.get_db_url_by_secret_key(db, secret_key):
        await crud.delete_db_url(db, db_url)
        return {"message": f"URL {db_url.target_url} has been deleted successfully!"}

    raise_not_found(request)
