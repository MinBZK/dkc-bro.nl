FROM python:3.12-alpine

RUN pip install pdm

FROM $BASE_IMAGE AS BUILDER
COPY ./backend/pyproject.toml ./backend/pdm.lock /backend/

WORKDIR /backend
RUN pdm install --prod --no-editable

FROM ${BASE_IMAGE}
COPY --from=BUILDER /backend/.venv /backend/.venv

ENV PATH="/backend/.venv/bin:$PATH"

COPY ./backend/app /backend/app
COPY ./backend/tests /backend/tests
COPY ./backend/start.sh /backend/start.sh

WORKDIR /backend
RUN chmod 777 ./start.sh

CMD ["./start.sh"]