FROM python:3.11.9

WORKDIR /automc

COPY . .

RUN pip install -r requirements.txt && \
    rm -f /automc/app/config.py alembic.ini

EXPOSE 3000

CMD ["./start.sh"]
