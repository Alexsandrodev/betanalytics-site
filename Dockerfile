FROM python:3.11

WORKDIR /tipsproject

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /tipsproject

COPY entrypoint.prod.sh /entrypoint.prod.sh

RUN chmod +x entrypoint.prod.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.prod.sh"]
