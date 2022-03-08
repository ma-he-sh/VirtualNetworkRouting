FROM python:3.8-alpine
RUN pip install flask
RUN pip install python-dotenv
RUN pip install coloram

COPY . .

ENTRYPOINT [ "python" ]
CMD ["/router/router.py"]