#Python
from typing import Optional
from enum import Enum

#pydantic
from pydantic import BaseModel , Field , EmailStr , HttpUrl

#FastAPI
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Body, Header, Path, Query, UploadFile , status,Form , Cookie,File


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
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary="Home page"
    )
def home():
    """Home Page

    This path returns the home page of the API

    No parameters are required 
    """
    return {"Hello": "World"}

# Request and Response body 

@app.post(
    path="/person/new",
    response_model=PersonBase,
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create person in the app"
    )
def create_person(person: PersonBase= Body(...)): 
    """
    Create Person

    This path operation creates a peron in the app and save the information in the database

    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name , age , hair color,marital status and email.
    
    Returns a person model with first name, last name , age hair color, marital status and email.
    """
    return person

#Validations: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Get person detail",
    deprecated=True
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
    """Show Person

    This path operation shows the person's name and age in the app from data base 

    Parameters:
    - Query parameter:
        - **name : str** -> this is the person name, It's between 1 and 50 characters
        - **age : int** -> this is the person age, It's required

    Returns:
        - A JSON with the person's name and age.
    """
    return {name:age}

#Validataion: Path Parameters
persons=[1,2,3,4,5,6]


@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Get person ID"
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the person ID,its required",
        example=12345

        )
):

    """Show person ID

    this path shows the person's ID in the app from the database

    Parameters:
    - path parameter:
        - **person_id:int** ->this is the person ID. It's required and must be greater than 0.
        
    Returns:
        A JSON with the person's ID.
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="!this person doesn't exist!"
        )

    return {person_id : "It Exists!"}

#Validations = Request Body

@app.put(
    path="/person/{person_id}",
    response_model=PersonBase,
    response_model_exclude={"password"},    
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Persons"],
    summary="Update Person"
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
    """Update Person

    This path operation updates the person's information form the database.

    Parameters:
    - Path parameter:
        - **person_id=int** -> this is the person ID, It's required and must be greater tha 0.
    - Request body parameter: 
        - **person:person** -> A person model with first name, last name , age , hair color,marital status and email.
        - **location : location** -> A location model wwith city,state and country.
        
    Returns:
        A JSON with the person's ID, it's model and location
    """
    result = person.dict()
    result.update(location.dict())
    return result

#Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Login"
)
def login(username: str = Form(...),password:str = Form(...) ):
    """User Login

    This path operation allows you to login in the app.

    Parameters:
    - Request body parameter:
        - **username: str** -> this is the username to enter in the form.It's required.
        - **password: str** -> this is the password to enter in the form. It's required
        
    Returns:
        A JSON with the usernamee and message.
    """
    return LoginOut(username=username)

# Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Forms"],
    summary="Contact"
    )
def contact(
    first_name:str=Form(
        ...,
        max_length=20,
        min_length=1
        ),
    last_name:str=Form(
        ...,
        max_length=20,
        min_length=1
        ),
    email: EmailStr = Form(...),
    message:str=Form(
        ...,
        min_length=20,
        ),
    user_agent:Optional[str] = Header(default=None),
    ads: Optional[str]= Cookie(default=None)        

):
    """Contact 

    This path operation allows the user to contact the company

    Parameters:
    - user_agent: the browser that the user is using.
    - ads : The cookies that this website uses.
    - Request body parameter:
        - **first_name : str** -> This is the first name to enter in the form. It's required.
        - **last_name : str** -> This is the last name to enter in the form. It's required.
        - **email : EmailStr**-> This is the email name to enter in the form. It's required.
        - **message : str** -> This is the message name to enter in the form. It's required.

    Returns:
        The header of the website
    """
    return user_agent 


# files 


@app.post(
    path="/post-image",
    tags=["Files"],
    summary="Post Image"
    )
def post_image(
    image: UploadFile = File(...)
):
    """Post image

    this path operations allows you to post an image in the app to the database

    Parameters:
    - Request body parameter:
        - **image: UploadFile** -> this is the image to upload, It's required

    Returns:
        A JSON with the image's name,format and size in kb
    """
    return {
        "Filename" : image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len( image.file.read())/1024,ndigits=2)
    }

