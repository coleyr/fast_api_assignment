FROM python:3.10

WORKDIR /usr/src/app/

COPY ./app /usr/src/app/

RUN  aptDep='git nano' \
    && apt-get update && apt-get install -y $aptDep --no-install-recommends --fix-missing \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt 

EXPOSE 9000

ENTRYPOINT [ "./entrypoint.sh" ]