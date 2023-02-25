# Stage 1: Build the application
FROM python:3.10-slim-buster AS builder

# make a new folder inside container
WORKDIR /backend-flask

# this contains the libraries want to install to run the app
COPY requirements.txt requirements.txt

# Install the python libraries used for the app
RUN pip3 install -r requirements.txt

# Outside Container -> Inside Container
# . means everything in the current directory
# 1st . -> /backend-flask (outside container)
# 2nd . -> /backend-flask (inside container)
COPY . .

# Set Environment Variables (Env Vars)
ENV FLASK_ENV=development

# Stage 2: Create the final image
FROM python:3.10-slim-buster

# make a new folder inside container
WORKDIR /backend-flask

# Copy only the built files from the previous stage
COPY --from=builder /backend-flask .

EXPOSE ${PORT}

# CMD (Command)
# python3 -m flask run --host=0.0.0.0 --port=4567
# -m -> module
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
