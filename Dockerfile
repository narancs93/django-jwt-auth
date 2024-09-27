FROM docker.io/python:3.12.6-slim-bookworm AS python

# Python build stage
FROM python AS python-build-stage

RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg dependencies
    libpq-dev

# Create Python Dependency and Sub-Dependency Wheels.
COPY requirements.txt .
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
    -r requirements.txt


# Python 'run' stage
FROM python AS python-run-stage

ARG APP_HOME=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR ${APP_HOME}

# devcontainer dependencies and utils
RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh

# Create devcontainer user and add it to sudoers
RUN groupadd --gid 1000 dev-user \
    && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
    && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
    && chmod 0440 /etc/sudoers.d/dev-user

RUN apt-get update && apt-get install --no-install-recommends -y \
    # psycopg dependencies
    libpq-dev \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./entrypoint /entrypoint
RUN chmod +x /entrypoint

COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]