import re
import sys
import requests
from fastapi import FastAPI, HTTPException, Request, status
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
                    datefmt='%Y-%m-%d,%H:%M:%S', filename=logfile)


# Instatiate model for request proxy
class post_call(BaseModel):
    '''Looks for url in json param and is used for post request'''
    url: str  # A url string for a get request

#Instatiate class instance of FastApi
app = FastAPI()
#Set header dict to be used by all requests
headers = {"Accept": "application/json"}
#Use regex to validate url's submitted in /ping post requests
valid_html_regex = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
def validate_http(url:str) -> bool:
    '''
Returns a boolean, True if the str provided is a valid url.

        Parameters:
                url (str): A url string

        Returns:
                valid (bool): A boolean based off the regex search of the url
    '''
    valid = bool(valid_html_regex.search(url))
    if not valid:
        logging.info(f"Invalid http request detected in url provided: {url}")
    return valid

#Custom Error handling....mhmmmm donuts
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    '''
    Returns a normal exception msg after logging and printing a custom message.

        Parameters:
                request (Request): A starlette Request object
                exc (HttpException): A httpexception object 
        Returns:
                http_exception_handler (func response): await http_exception_handler(request, exc)
    '''
    print(f"Doh! An HTTP error!: {repr(exc)}")
    logging.warning(f"Doh! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)

#Custom Error handling, with a concise message for our use case
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    '''
    Returns a normal exception msg after logging and printing a custom message.

        Parameters:
                request (Request): A starlette Request object
                exc (RequestValidationError): A RequestValidationError object 
        Returns:
                validation_exception_handler response (func response): await validation_exception_handler(request, exc)
    '''
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
    '''
    Returns a static dict in the form of json response

        Parameters:
                None
        Returns:
                {"Receiver": "Cisco is the best!"} (json response): a json string of the static dict
    '''
    return {"Receiver": "Cisco is the best!"}

#Route decorator and function for root, returns a static dict
@app.get("/")
async def root():
    '''
    Returns a static dict in the form of json response

        Parameters:
                None
        Returns:
                {"message": "FastApi for interview"} (json response): a json string of the static dict
    '''
    return {"message": "FastApi for interview"}

#Helper function for calling the request library, all request exceptions included
def call_url(url: str) -> requests.Response | requests.RequestException:
    '''
Returns a request response in a json formated dict.

        Parameters:
                url (str): A url string

        Returns:
                reponse (dict): A request reponse object formatted as a json dict
    '''
    logging.info(f"Attempted call to {url}")
    try:
        response = requests.get(url, verify=False, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.warning(f"call to {url} failed")
        return {'exception': e}
    
#Post function for route ping, calls body url if body url present
@app.post("/ping")
async def ping(body: post_call) -> requests.Response|dict:
    '''
    Takes the json body from a post and searchs for an url attribute:
    Returns a request response in a json formated dict. Checks for valid url.

        Parameters:
                body (post_call): A post_call model object

        Returns:
                reponse (dict): A request reponse object formatted as a json dict
    '''
    return (
        (call_url(body.url))
        if validate_http(body.url)
        else {
            "Doh!": f"Invalid http request detected in url provided: {body.url}"
        }
    )

#Just a bit of fun, a static call to get a random chuck norris joke
@app.get("/chuck")
async def get_chuck() -> requests.Response|dict:
    '''
    Returns a request response in a json formated dict from a call to a 
    Chuck Norris joke api https://api.chucknorris.io/jokes/random

        Parameters:
                None

        Returns:
                reponse (dict): A request reponse object formatted as a json dict, contains a joke 
    '''
    return call_url("https://api.chucknorris.io/jokes/random")

#Just a bit of fun, a static call to get a random simpsons quote
@app.get("/simpsons_quote")
async def get_simpsons_quote() -> requests.Response|dict:
    '''
    Returns a request response in a json formated dict from a call to a 
    simpsons quote api https://thesimpsonsquoteapi.glitch.me/quotes

        Parameters:
                None

        Returns:
                reponse (dict): A request reponse object formatted as a json dict, contains a simpsons quote
    '''
    return call_url("https://thesimpsonsquoteapi.glitch.me/quotes")

#Just a bit of fun, a static call to get a random dad joke api
@app.get("/dad_joke")
async def get_dad_joke() -> requests.Response|dict:
    '''
    Returns a request response in a json formated dict from a call to a 
    dad joke api https://icanhazdadjoke.com/

        Parameters:
                None

        Returns:
                reponse (dict): A request reponse object formatted as a json dict, contains a dad joke
    '''
    return call_url("https://icanhazdadjoke.com/")