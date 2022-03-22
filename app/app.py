import re
import requests
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
import logging

#Setup logging for application
format = "%(asctime)s %(name)10s %(levelname)8s: %(message)s"
logfile="api_activity.log"
logging.basicConfig(format=format, level=logging.DEBUG,
                    datefmt="%H:%M:%S", filename=logfile)


# Instatiate model for request proxy
class post_call(BaseModel):
    '''Looks for url in json param and is used for post request'''
    url: str  # A url string for a get request

#Instatiate class instance of FastApi
app = FastAPI()
headers = {"Accept": "application/json"}
#Use regex to validate url's submitted in /ping post requests
valid_html_regex = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
def validate_http(url:str) -> bool:
    '''params: url: http url string
    returns a bool if the url given is a valid url'''
    valid = bool(valid_html_regex.search(url))
    if not valid:
        logging.info(f"Invalid http request detected in url provided: {url}")
    return valid

#Custom Error handling....mhmmmm donuts
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"Doh! An HTTP error!: {repr(exc)}")
    logging.warning(f"Doh! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)

#Custom Error handling, with a concise message for our use case
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    msg = f"Doh!: No 'url' attribute in request body {exc.body}\n" if request.method == 'POST' else ""
    output = {"msg": msg, "detail": exc.errors()}
    logging.warning(output)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(output),
    )

#Route decorator and function for info, returns a static dict
@app.get("/info")
async def info():
    return {"Receiver": "Cisco is the best!"}

#Route decorator and function for root, returns a static dict
@app.get("/")
async def root():
    return {"message": "FastApi for interview"}

#Helper function for calling the request library, all request exceptions included
def call_url(url):
    logging.info(f"Attempted call to {url}")
    try:
        response = requests.get(url, verify=False, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.warning(f"call to {url} failed")
        return e
    
#Post function for route ping, calls body url if body url present
@app.post("/ping")
async def ping(body: post_call):
    return (
        (call_url(body.url))
        if validate_http(body.url)
        else {
            "Doh!": f"Invalid http request detected in url provided: {body.url}"
        }
    )

#Just a bit of fun, a static call to get a random chuck norris joke
@app.get("/chuck")
async def get_chuck():
    return call_url("https://api.chucknorris.io/jokes/random")

#Just a bit of fun, a static call to get a random simpsons quote
@app.get("/simpsons_quote")
async def get_simpsons_quote():
    return call_url("https://thesimpsonsquoteapi.glitch.me/quotes")

#Just a bit of fun, a static call to get a random dad joke api
@app.get("/dad_joke")
async def get_dad_joke():
    return call_url("https://icanhazdadjoke.com/")