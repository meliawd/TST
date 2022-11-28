from fastapi import FastAPI
from pydantic import BaseModel

import json

app = FastAPI()
auth_handler = AuthHandler()
users = []

@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password    
    })
    return


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }

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

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)