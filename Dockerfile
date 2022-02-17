FROM python:3.9-slim-bullseye
ADD . /mdmail
RUN pip install /mdmail && rm --recursive --force /mdmail "$(pip cache dir)"
ENTRYPOINT ["mdmail"]
CMD ["--help"]
