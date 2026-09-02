# shortener_app/crud.py

from sqlalchemy.orm import Session
from . import keygen, models, schemas

def create_db_url(db : Session, url: schemas.URLBase) -> models.URL:
    key = keygen.create_nique_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    
    db_url = models.URL(
        key=key,
        secret_key=secret_key,
        target_url=url.target_url
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_key(db: Session, key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == key, models.URL.is_active == True)
        .first()
    )