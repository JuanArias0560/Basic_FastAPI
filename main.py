#Python
from typing import Optional
#pydantic
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI,Body, Path, Query


app = FastAPI()

#Models

class Person(BaseModel):
    first_name  : str 
    last_name   : str
    age         : int
    hair_color  : Optional[str]  =  None
    is_married  : Optional[bool] =  None

class Location(BaseModel):
    city  : str
    state : str
    country :str

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



