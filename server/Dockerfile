FROM python:3.8-alpine
RUN pip install flask
RUN pip install python-dotenv
RUN pip install colorama

COPY . .

ENTRYPOINT ["python"]
CMD ["/app/server.py"]