# Docker container for Bot1
FROM python:latest

WORKDIR .

RUN mkdir src
COPY src/* ./src/
COPY requirements.txt .
COPY .env .
COPY setup.py .
COPY Makefile .

RUN make install
RUN make install_deps

CMD [ "cointbot", "-c", "usdt"]