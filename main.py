from fastapi import FastAPI
from pydantic import BaseModel

import json

app = FastAPI()

class beasiswa(BaseModel):
    Beasiswa : str
    Indeks : float
    UKT : int
    Gaji : int

@app.post("/")
async def add_beasiswa(b: beasiswa):
    list_beasiswa = []

    with open('beasiswa.json', 'r') as f:
        list_beasiswa = json.load(f)['beasiswa']

    new_beasiswa = {
        "Beasiswa" : b.Beasiswa,
        "Indeks" : b.Indeks,
        "UKT" : b.UKT,
        "Gaji" : b.Gaji
        }

    list_beasiswa.append(new_beasiswa)

    output = {'beasiswa':list_beasiswa}
    with open('beasiswa.json', 'w') as f:
        json.dump(output, f)

    return "Data beasiswa baru: " +str(new_beasiswa)+ " telah diterima"
