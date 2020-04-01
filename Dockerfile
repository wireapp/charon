# ----------- download python dependencies -----------
FROM python:3.7-alpine AS install
# install pipenv
RUN pip install pipenv

# copy dependencies
COPY Pipfile* /

# install dependencies
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

# ----------------------Final image-------------------
FROM python:3.7-alpine AS image
# copy dependencies
COPY --from=install /usr/local /usr/local

# copy app
COPY . /app/
WORKDIR /app

# create version file
ARG release_version=development
ENV RELEASE_FILE_PATH=/app/release.txt
RUN echo $release_version > $RELEASE_FILE_PATH

# start app
EXPOSE 8080
CMD gunicorn --bind 0.0.0.0:8080 app:app