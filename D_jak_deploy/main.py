from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import hashlib
from typing import Optional
from datetime import date, timedelta

app = FastAPI()
app.counter = 0
app.patient_counter = 0


class HelloResp(BaseModel):
    msg: str


class Patient(BaseModel):
    id: Optional[int] = None
    name: str
    surname: str
    register_date: Optional[date] = None
    vaccination_date: Optional[date] = None


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter


@app.get("/hello/{name}", response_model=HelloResp)
async def read_item(name: str):
    return HelloResp(msg=f"Hello {name}")


@app.api_route("/method", methods=["GET", "POST", "DELETE", "OPTIONS", "PUT"])
def method(request: Request, response: Response):
    if request.method == "POST":
        response.status_code = 201
    else:
        response.status_code = 200
    return {"method": request.method}


@app.get("/auth/")
async def auth(
    response: Response,
    password: Optional[str] = None,
    password_hash: Optional[str] = None,
):
    if (
        password is None
        or password_hash is None
        or password == ""
        or password_hash == ""
    ):
        response.status_code = 401
        return
    hash = hashlib.sha512(password.encode("utf-8")).hexdigest()
    if hash == password_hash:
        response.status_code = 204
    else:
        response.status_code = 401


@app.post("/register/")
async def register(response: Response, patient: Patient):
    app.patient_counter += 1
    patient.id = app.patient_counter
    patient.register_date = date.today().isoformat()
    vaccination_date = date.today() + timedelta(
        days=(len(patient.name) + len(patient.surname))
    )
    patient.vaccination_date = vaccination_date
    response.status_code = 201
    return patient.dict()
