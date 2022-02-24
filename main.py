#Python
from typing import Optional
from enum import Enum
#pydantic
from pydantic import BaseModel , Field , EmailStr , HttpUrl
#FastAPI
from fastapi import FastAPI,Body, Path, Query 


app = FastAPI()

#Models

class HairColor(Enum):
    white="White"
    brown="Brown"
    black="Black"
    blonde="blonde"
    red="red"


class Person(BaseModel):

    first_name  : str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    last_name   : str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    age         : int = Field(
        ...,
        gt=0,
        le=115
        )
    hair_color  : Optional[HairColor]  =  Field(default=None)
    is_married  : Optional[bool] =  Field(default=None)
    email : EmailStr = Field(...)
    http : HttpUrl = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "first_name": "Juan",
                "last_name" : "Arias Saldaña",
                "age": 24,
                "hair_color": "blonde",
                "is_married" : True,
                "email" : "juan@juan.com",
                "http" : "http://juan.com"
            }
        }

class Location(BaseModel):
    city  : str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    state : str= Field(
        ...,
        min_length=1,
        max_length=50,
        )
    country :str= Field(
        ...,
        min_length=1,
        max_length=50,
        )
    class Config:
        schema_extra={
            "example":{
                "city": "Bogota",
                "state" : "Cundinamarca",
                "country" : "Colombia"
            }
        } 

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response body 

@app.post("/person/new")
def create_person(person: Person = Body(...)): 
    return person

#Validations: Query Parameters

@app.get("/person/detail")
def show_person(
    name:Optional[str]= Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"

        )
):
 return {name:age}

#Validataion: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the person ID,its required"
        )
):
    return {person_id : "It Exists!"}

#Validations = Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int =Path(
        ...,
        title="Person Id",
        description="This is the person ID",
        gt=0
    ), 
    person: Person = Body(...),
    location: Location = Body(...)

):
    result = person.dict()
    result.update(location.dict())
    return result



