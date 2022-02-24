FROM python:3.8-alpine
RUN pip install flask
RUN pip install python-dotenv
RUN pip install colorama

WORKDIR /server

COPY ./app /server

ENTRYPOINT ["python"]
CMD ["server.py"]