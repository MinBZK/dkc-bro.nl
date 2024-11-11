FROM python:3.12-alpine

RUN pip install pdm

COPY ./backend/pyproject.toml ./backend/pdm.lock /backend/

WORKDIR /backend
RUN pdm install --prod --no-editable

ENV PATH="/backend/.venv/bin:$PATH"

COPY ./backend/app /backend/app
COPY ./backend/tests /backend/tests
COPY ./backend/start.sh /backend/start.sh

RUN chmod 777 ./start.sh

CMD ["./start.sh"]