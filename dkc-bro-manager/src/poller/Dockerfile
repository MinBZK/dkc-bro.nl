FROM python:3.12-alpine
FROM $BASE_IMAGE AS BUILDER
COPY ./pyproject.toml ./pdm.lock /poller/

RUN pip install pdm

WORKDIR /poller
RUN pdm install --prod --no-editable

FROM ${BASE_IMAGE}
COPY --from=BUILDER /poller/.venv /poller/.venv

ENV PATH="/poller/.venv/bin:$PATH"

COPY ./app ./poller/app

WORKDIR /poller

CMD ["python", "-m", "app"]