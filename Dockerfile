FROM python:3.7

WORKDIR /app
COPY requirements-dev.txt setup.cfg setup.py ./
COPY django_alive/__init__.py ./django_alive
RUN python -m pip install -r requirements-dev.txt -e .
CMD pytest
COPY . .
