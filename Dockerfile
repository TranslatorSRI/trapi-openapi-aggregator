FROM renciorg/renci-python-image:v0.0.1

RUN mkdir /code
WORKDIR /code


# install requirements
ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/ src/
COPY servers.json servers.json
RUN chmod 777 ./

USER nru
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8080" , "--workers", "1", "--app-dir", "/code/",  "src.server:app"]