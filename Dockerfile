FROM ubuntu

RUN apt update
RUN apt install python3-pip -y
RUN apt update
RUN pip install -r requirements.txt


WORKDIR /app

COPY . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]