FROM python:3.11.9

WORKDIR /automc

COPY . .

RUN pip install -r requirements.txt && \
    rm /automc/app/config.py /automc/app/config.py

EXPOSE 3000

CMD ["./start.sh"]
