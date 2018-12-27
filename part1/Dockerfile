FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY dataProcessor.py /usr/src/app
CMD [ "python", "dataProcessor.py" ,"1"]