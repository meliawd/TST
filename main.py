from fastapi import FastAPI
from pydantic import BaseModel

import json

app = FastAPI()

class mahasiswa(BaseModel):
    nim: int
    nama: str