FROM jupyter/datascience-notebook
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY analysis.ipynb /usr/src/app
EXPOSE 8888
CMD [ "jupyter", "notebook","--allow-root" ]