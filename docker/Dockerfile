FROM downloads.unstructured.io/unstructured-io/unstructured:latest
ENV HOME=/home/notebook-user
WORKDIR ${HOME}
COPY requirements.txt ${HOME}/requirements.txt
RUN python3 -m pip install -r requirements.txt