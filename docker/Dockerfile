FROM python:3.11-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Seoul
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y software-properties-common python3-launchpadlib \
  && add-apt-repository ppa:libreoffice/ppa \
  && apt-get -y install tzdata fontconfig fonts-nanum libreoffice \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean \
  && fc-cache -fv

COPY --from=requirements-stage /wheels /wheels
COPY --from=requirements-stage /tmp/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache /wheels/*

COPY ./project .
COPY ./bin/entrypoint.sh ./bin/entrypoint.sh

EXPOSE 8000

RUN chmod +x ./bin/entrypoint.sh
ENTRYPOINT ["./bin/entrypoint.sh"]
