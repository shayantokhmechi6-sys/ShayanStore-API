from fastapi import FastAPI
from database import engine,Base
import models

app=FastAPI()

SECRET_KEY="my-super-secret-key"

Base.metadata.create_all(engine)
