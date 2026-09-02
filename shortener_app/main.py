# shortener_app/main.py

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from . import models, schemas
from .database import SessionLocal, engine
from . import crud
from .config import get_settings    

app = FastAPI()
""" 
    Binds your database engine with models.Base.metadata.create_all(). 
    If the database that you defined in engine doesn’t exist yet, 
    then it’ll be created with all modeled tables once you run your 
    app the first time. 
"""
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "Administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url

def raise_bad_request(message) :
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    message = f'URL {request.url } Not Found!'
    raise HTTPException(status_code=404, detail=message)

@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_key(db, url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    db_url = crud.create_db_url(db=db, url=url)

    return get_admin_info(db_url)

@app.get(
    "/admin/{secret_key}",
    name = "Administration info",
    response_model = schemas.URLInfo
)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)