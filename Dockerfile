# ----------- download python dependencies -----------
FROM python:3.7-alpine AS install
# install pipenv
RUN pip install pipenv
# create application folder
RUN mkdir /app
WORKDIR /app

# copy dependencies
COPY Pipfile* /app/

# install dependencies
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

# ----------------------Final image--------------------------------
FROM install AS image
# copy dependencies
COPY --from=install /usr/local /usr/local
# copy app
COPY . /app/

# start app
EXPOSE 8080
ENV FLAS_APP=app
ENV FLAS_ENV=production
CMD flask run --port=8080 --host=0.0.0.0