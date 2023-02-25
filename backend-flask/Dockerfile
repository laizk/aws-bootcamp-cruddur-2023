# Stage 1: Install dependencies
FROM python:3.10-slim-buster AS build-base

# Inside Container
# make a new folder inside container
WORKDIR /backend-flask

# Outside Container -> Inside Container
# . means everything in the current directory
# 1st . -> /backend-flask (outside container)
# 2nd . -> /backend-flask (inside container)
COPY . .

# Outside Container -> Inside Container
# this contains the libraries want to install to run the app
COPY requirements.txt .

# Inside Container
# Install the python libraries used for the app
RUN pip3 install --user -r requirements.txt

# Stage 2: Copy the dependencies from stage 1 and run application
FROM python:3.10-slim-buster AS release
WORKDIR /backend-flask

COPY --from=build-base /root/.local /root/.local
COPY --from=build-base /backend-flask /backend-flask

ENV PATH=/root/.local:$PATH

EXPOSE ${PORT}

# CMD (Command)
# python3 -m flask run --host=0.0.0.0 --port=4567
# -m -> module
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]