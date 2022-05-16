from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
import calendar
import datetime


class HerokuApp:
    app_url = "http://127.0.0.1:8000"

app = FastAPI()
app.counter = 0

# @app.get("/")
# def root():
#     return {"msg": "Hello World"}

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
