#Python
from email.policy import default
from typing import Optional
from enum import Enum
#pydantic
from pydantic import BaseModel , Field , EmailStr , HttpUrl
#FastAPI
from fastapi import FastAPI,Body, Path, Query , status,Form


app = FastAPI()

#Models

class HairColor(Enum):
    white="White"
    brown="Brown"
    black="Black"
    blonde="blonde"
    red="red"


class PersonBase(BaseModel):

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
    password: str = Field(
        ...,
        min_length=8,        
        )


    class Config:
        schema_extra = {
            "example":{
                "first_name": "Juan",
                "last_name" : "Arias Saldaña",
                "age": 24,
                "hair_color": "blonde",
                "is_married" : True,
                "email" : "juan@juan.com",
                "http" : "http://juan.com",
                "password":"Ju63bao345"
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


class LoginOut(BaseModel):
    username: str = Field(...,max_length=20,example="JuanArias")
    massage: str = Field(default="Login Succesfully")

@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "World"}

# Request and Response body 

@app.post(
    path="/person/new",
    response_model=PersonBase,
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: PersonBase= Body(...)): 
    return person

#Validations: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name:Optional[str]= Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Jheraldyn"
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=26

        )
):
 return {name:age}

#Validataion: Path Parameters

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the person ID,its required",
        example=12345

        )
):
    return {person_id : "It Exists!"}

#Validations = Request Body

@app.put(
    path="/person/{person_id}",
    response_model=PersonBase,
    response_model_exclude={"password"},    
    status_code=status.HTTP_202_ACCEPTED
)
def update_person(
    person_id: int =Path(
        ...,
        title="Person Id",
        description="This is the person ID",
        gt=0,
        example=12345
    ), 
    person: PersonBase = Body(...),
    location: Location = Body(...)

):
    result = person.dict()
    result.update(location.dict())
    return result

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...),password:str = Form(...) ):
    return LoginOut(username=username)

