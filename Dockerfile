FROM python:3.10

EXPOSE 3214

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install -y \
    libgl1-mesa-glx

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]