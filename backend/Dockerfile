FROM python:3.9

WORKDIR /app

RUN pip install poetry==1.1.13

COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./src /app

ARG mongodb_hosts
ARG mongodb_user
ARG mongodb_password
ARG flask_env
ARG aws_bucket
ARG aws_access_key_id
ARG aws_secret_access_key
ARG jwt_secret_key

ENV MONGODB_HOSTS $mongodb_hosts
ENV MONGODB_USER $mongodb_user
ENV MONGODB_PASSWORD $mongodb_password
ENV AWS_BUCKET $aws_bucket
ENV AWS_ACCESS_KEY_ID $aws_access_key_id
ENV AWS_SECRET_ACCESS_KEY $aws_secret_access_key
ENV FLASK_ENV $flask_env
ENV JWT_SECRET_KEY $jwt_secret_key


CMD python app.py