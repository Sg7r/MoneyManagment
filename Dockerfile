FROM python:3.11-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# set a directory for the app
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy all the files to the container
COPY . .
COPY entrypoint.sh /app/entrypoint.sh


# Copy and make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# run the command
CMD ["gunicorn", "moneyManagment.wsgi:application", "--bind", "0.0.0.0:8000"]
