FROM python:3.12-alpine
COPY ./pyproject.toml ./pdm.lock /poller/

RUN pip install pdm

WORKDIR /poller
RUN pdm install --prod --no-editable

ENV PATH="/poller/.venv/bin:$PATH"

COPY ./app ./app

CMD ["python", "-m", "app"]