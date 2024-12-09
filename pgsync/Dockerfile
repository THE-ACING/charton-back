FROM python:3.9

ARG WORKDIR=/code
WORKDIR $WORKDIR

RUN pip install git+https://github.com/toluaina/pgsync.git

COPY . .

RUN chmod +x entrypoint.sh
RUN chmod +x wait-for-it.sh

ENTRYPOINT ["./entrypoint.sh"]