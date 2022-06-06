from fastapi import FastAPI, HTTPException, Response, status, Depends, Request, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field
import calendar
import datetime


from fastapi import FastAPI

from .views import router as northwind_api_router

app = FastAPI()

app.include_router(northwind_api_router, tags=["northwind"])

app.counter = 0


class HerokuApp:
    app_url = "http://127.0.0.1:8000/"

# ZAD 1.1

@app.get("/")
def root():
    return {"start": "1970-01-01"}


# ZAD 1.2

@app.get("/method")
def get_method():
    return {"method": "GET"}

@app.post("/method", status_code=201)
def post_method():
    return {"method": "POST"}

@app.put("/method")
def put_method():
    return {"method": "PUT"}

@app.options("/method")
def options_method():
    return {"method": "OPTIONS"}

@app.delete("/method")
def delete_method():
    return {"method": "DELETE"}


# ZAD 1.3

@app.get("/day")
async def check_correct(name: str, number: int):
    if calendar.day_name[number-1] == name.capitalize():
        return {
            "name": name,
            "number": number,
                }
    else:
        raise HTTPException(status_code=400,detail="Bad Request")


# ZAD 1.4

events = []

class Item(BaseModel):
    id: int | None = -1
    name: str  = Field(alias="event")
    date: str
    date_added: str | None = datetime.date.today()

class Config:
    allow_population_by_field_name = True


@app.put("/events/")
async def save_event(item: Item):
    item_json = item.dict()
    item_json["id"] = app.counter
    app.counter += 1
    events.append(item_json)
    return item_json


# ZAD 1.5

@app.get("/events/{date}")
def show_event(date: str, response: Response):

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response
    else:

        result = []

        for event in events:
            if event["date"] == date:
                result.append(event)
        if len(result) == 0:
                    response.status_code = status.HTTP_404_NOT_FOUND
                    return response
        else:
            return result



# ZAD 3.1

@app.get("/start", response_class=HTMLResponse)
def index_start():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>The unix epoch started at 1970-01-01</h1>
        </body>
    </html>
    """


# ZAD 3.2

security = HTTPBasic()

@app.post("/check", response_class=HTMLResponse)
def check_your_age(response: Response, credentials: HTTPBasicCredentials = Depends(security)):


    name = credentials.username
    birthdate = credentials.password

    today = datetime.date.today()
    data = birthdate.split("-")
    age = today.year - int(data[0]) - ((today.month, today.day) < (int(data[1]), int(data[2])))
    
    if age < 16:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    else:
        return f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Welcome {name}! You are {age}</h1>
        </body>
    </html>
    """


# ZAD 3.3

@app.get("/info")
def information(response: Response, format: str | None = None, user_agent: str | None = Header(default=None)):
    if format == "json":
        print("I get a json")
        response = {
                    "user_agent": f"{user_agent}"
                    }   
        return response
    elif format == "html":
        
        print("I get a html")
        response = f"""
        <html>
            <head>
                <title>Some HTML in here</title>
            </head>
            <body>

                <h1><input type="text" id=user-agent name=agent value="{user_agent}"></h1>
            </body>
        </html>
        """
        return HTMLResponse(content=response, status_code=200)
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response


# ZAD 3.4



list_of_paths = []

@app.get("/save/{string}", response_class=RedirectResponse, status_code=301)
def redirect_typer(string: str, response:Response):
    if f"/save/{string}" in list_of_paths:
        return "http://127.0.0.1:8000/info?format=json"
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response


@app.put("/save/{string}", status_code=200)
def record_paths(string: str, response:Response):
    path_copy = f"/save/{string}"
    print(path_copy)
    list_of_paths.append(path_copy)
    response = "Path saved"
    return response


@app.delete("/save/{string}")
def delete_path(string: str, response:Response):
    flag1 = True
    for item in list_of_paths:
        if item == f"/save/{string}":
            flag1 = False
            list_of_paths.remove(item)
            response = "Path deleted"
            return response
    if flag1:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    

@app.post("/save/{string}")
@app.patch("/save/{string}")
def bad_request(response:Response):
    response.status_code = status.HTTP_400_BAD_REQUEST
    return response




# ZAD 5.1


