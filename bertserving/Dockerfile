FROM tensorflow/tensorflow:1.12.0-py3
RUN pip install -U pip
RUN pip install --no-cache-dir bert-serving-server==1.9.8
WORKDIR /bert
COPY . /bert
RUN chmod +x bert.sh

CMD ["./bert.sh"]