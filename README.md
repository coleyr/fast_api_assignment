# fast_api_assignment
A fast API application to fulfill the prompt for the upcoming interview

# Table of Contents
1. [Synopsis](#Synopsis)
2. [Live Demo](#Live_Links)
3. [Install Instructions](#Install)
4. [API Path Table](#API)


## Synopsis
### an api built with fastapi to respond to certain api calls and demonstrate the use of a python web framework.

# Live_Links
### View the documentation
1. [API documentation](https://174.129.182.47/docs) (api swagger documentation)
2. [API documentation](https://174.129.182.47/redoc) (api redoc documentation)
### Test the API
    GET 174.129.182.47/ 

# Install
## [Development] Local machine
1. Install python https://www.python.org/downloads/
1. If using Windows, install git, preferably using chocolatey: https://chocolatey.org/ - `choco install git`
   1. Set end-of-line character - `git config --global core.eol lf`
   1. Disable end-of-line character conversion `git config --global core.autocrlf input`
1. Clone or download this repo `git clone https://github.com/coleyr/fast_api_assignment`
1. Navigate to the repo's folder on your local filesystem using a terminal
1. Navigate to the fast_api_assignment/app folder
1. Install dependecies with `python -m pip install -r requirements.txt`
1. Run the application with `uvicorn app:app --reload`
    1. optional:   
    --host TEXT                     Bind socket to this host.  [default:
                                  127.0.0.1]
    --port INTEGER                  Bind socket to this port.  [default: 8000]
    Additional options at: https://www.uvicorn.org/deployment/
## Docker   
### [Development] Mac & Windows Instructions
1. Install python https://www.python.org/downloads/
1. Download and install Docker Desktop: https://www.docker.com/products/docker-desktop
1. If using Windows, install git, preferably using chocolatey: https://chocolatey.org/ - `choco install git`
   1. Set end-of-line character - `git config --global core.eol lf`
   1. Disable end-of-line character conversion `git config --global core.autocrlf input`
1. Clone or download this repo `git clone https://github.com/coleyr/fast_api_assignment`
1. Navigate to the repo's folder on your local filesystem using a terminal
1. Install docker-compose with `python -m pip install docker-compose`
1. Deploy with Docker Desktop in development mode:
   1. Build images - `docker-compose build`
   1. Start services - `docker-compose up -d`
   1. Site can now be viewed at 127.0.0.1:9000/docs
   1. try to get the root of the api: curl 127.0.0.1:9000
### [Production] Mac & Windows Instructions
1. Install python https://www.python.org/downloads/
1. Download and install Docker Desktop: https://www.docker.com/products/docker-desktop
1. If using Windows, install git, preferably using chocolatey: https://chocolatey.org/ - `choco install git`
   1. Set end-of-line character - `git config --global core.eol lf`
   1. Disable end-of-line character conversion `git config --global core.autocrlf input`
1. Clone or download this repo `git clone https://github.com/coleyr/fast_api_assignment`
1. Navigate to the repo's folder on your local filesystem using a terminal
1. Install docker-compose with `python -m pip install docker-compose`
1. Deploy with Docker Desktop in development mode:
   1. Build images - `docker-compose -f docker-compose-nginx.yml build`
   1. Start services - `docker-compose -f docker-compose-nginx.yml up -d`
   1. Site can now be viewed at 127.0.0.1/docs
   1. try to get the root of the api: curl 127.0.0.1/

### [Development] Useful Commands

1. Wipe Everything (wipes volumes)
   1. Wipe Containers
      1. `docker container stop $(docker container ls -aq)`
      1. `docker container rm $(docker container ls -aq)`
   1. Wipe Images
      1. `docker image prune -a`
   1. Wipe Volumes
      1. `docker volume ls`
      1. `docker volume prune`
   1. Remove Networks
      1. `docker network prune`
1. Docker local system resource clean-up (wipes volumes)
   1. `docker system prune --force --volumes`
1. Fast Full Re-build (wipes volumes)
   1. `docker-compose down -v --remove-orphans`
   2. `docker-compose build --no-cache`
   3. `docker-compose up -d --force-recreate`
1. Follow All Logs
   1. `docker-compose logs --follow`

## API Path Table
#### Information also available at: https://174.129.182.47/docs
| Method | Path | Description |
| --- | --- | --- |
| GET | [/info](#getinfo) | Info |
| GET | [/](#get) | Root |
| POST | [/ping](#postping) | Ping |
| GET | [/chuck](#getchuck) | Get Chuck |
| GET | [/simpsons_quote](#getsimpsons_quote) | Get Simpsons Quote |
| GET | [/dad_joke](#getdad_joke) | Get Dad Joke |

# API
## API Reference Table
| Name | Path | Description |
| --- | --- | --- |
| HTTPValidationError | [#/components/schemas/HTTPValidationError](#componentsschemashttpvalidationerror) |  |
| ValidationError | [#/components/schemas/ValidationError](#componentsschemasvalidationerror) |  |
| post_call | [#/components/schemas/post_call](#componentsschemaspost_call) | Looks for url in json param and is used for post request |

## Path Details

***

### [GET]/info

- Summary
Info

- Description
Returns a static dict in the form of json response

    Parameters:
            None
    Returns:
            {"Receiver": "Cisco is the best!"} (json response): a json string of the static dict

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

***

### [GET]/

- Summary
Root

- Description
Returns a static dict in the form of json response

    Parameters:
            None
    Returns:
            {"message": "FastApi for interview"} (json response): a json string of the static dict

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

***

### [POST]/ping

- Summary
Ping

- Description
Takes the json body from a post and searchs for an url attribute:
Returns a request response in a json formated dict. Checks for valid url.

    Parameters:
            body (post_call): A post_call model object

    Returns:
            reponse (dict): A request reponse object formatted as a json dict

#### RequestBody

- application/json

```ts
// Looks for url in json param and is used for post request
{
  url: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: string[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/chuck

- Summary
Get Chuck

- Description
Returns a request response in a json formated dict from a call to a
Chuck Norris joke api https://api.chucknorris.io/jokes/random

    Parameters:
            None

    Returns:
            reponse (dict): A request reponse object formatted as a json dict, contains a joke

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

***

### [GET]/simpsons_quote

- Summary
Get Simpsons Quote

- Description
Returns a request response in a json formated dict from a call to a
simpsons quote api https://thesimpsonsquoteapi.glitch.me/quotes

    Parameters:
            None

    Returns:
            reponse (dict): A request reponse object formatted as a json dict, contains a simpsons quote

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

***

### [GET]/dad_joke

- Summary
Get Dad Joke

- Description
Returns a request response in a json formated dict from a call to a
dad joke api https://icanhazdadjoke.com/

    Parameters:
            None

    Returns:
            reponse (dict): A request reponse object formatted as a json dict, contains a dad joke

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

## References

### #/components/schemas/HTTPValidationError

```ts
{
  detail: {
    loc?: string[]
    msg: string
    type: string
  }[]
}
```

### #/components/schemas/ValidationError

```ts
{
  loc?: string[]
  msg: string
  type: string
}
```

### #/components/schemas/post_call

```ts
// Looks for url in json param and is used for post request
{
  url: string
}
```