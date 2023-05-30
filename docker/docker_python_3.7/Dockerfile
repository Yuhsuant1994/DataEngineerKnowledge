FROM python:3.9-slim-buster
WORKDIR /code
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./src ./src
# CMD python3 src/hello.py
CMD ["python3", "./src/hello.py"; "tail", "-f", "/dev/null"]
