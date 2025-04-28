FROM python:3.11-slim

# set a directory for the app
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy all the files to the container
COPY . .

# run the command
CMD ["gunicorn", "moneyManagment.wsgi:application", "--bind", "0.0.0.0:8000"]
