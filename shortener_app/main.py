# shortener_app/main.py

import validators
from fastapi import FastAPI, HTTPException

from . import schemas

app = FastAPI()

@app.get("/")
def read_root():
    return "Welcome to the URL Shortener API!"

def raise_bad_request(message) :
    raise HTTPException(status_code=400, detail=message)

@app.post("/url")
def create_url(url : schemas.URLBase):
    if not validators.url(url.target_url) :
        raise_bad_request("The URL you provided is not valid.")
    return f"TODO: create database entry for {url.target_url}"