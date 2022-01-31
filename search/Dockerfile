FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
RUN chmod +x wait-for-it.sh
RUN chmod +x search.sh
RUN chmod +x autofill.sh