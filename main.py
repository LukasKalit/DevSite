from fastapi import FastAPI


class HerokuApp:
    app_url = "https://devsite-daftcode.herokuapp.com/"

app = FastAPI()

# @app.get("/")
# def root():
#     return {"msg": "Hello World"}

@app.get("/")
def root():
    return {"start": "1970-01-01"}


@app.get("/hello/{name}")
async def read_item(name: str):
    return f"Hello {name}"
