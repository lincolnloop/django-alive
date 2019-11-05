FROM python:3.7

WORKDIR /app
RUN pip install -U pipenv
COPY Pipfile Pipfile.lock setup.cfg setup.py ./
COPY django_alive/__init__.py ./django_alive
RUN pipenv install
ENV PATH=/root/.local/share/virtualenvs/app-4PlAip0Q/bin:${PATH}
CMD pytest
COPY . .
