FROM python:3.9-slim-buster




# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /app

## Copy the .aws folder with the credentials file into the container
#COPY .aws /root/.aws

#to COPY the remote file at working directory in container
COPY * ./
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc
#installing the dependencies
RUN pip install -r requirements.txt
#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

#CMD ["python3", "-m", "server", "--host=0.0.0.0", "--port=443"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "app:app"]