FROM svdh4blend/pyenv-pipenv-baseimage:latest
EXPOSE 8080
RUN mkdir /tmp/pypackage

COPY Pipfile.lock Pipfile ./
RUN pipenv sync

COPY pystock/ ./pystock
CMD PYTHONPATH=. pipenv run gunicorn pystock.server:app