FROM python:3.6-buster

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

RUN pip3 install --upgrade virtualenv && \
    virtualenv /env -p python3
#
## Setting these environment variables are the same as running
## source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD requirements.txt /rundir/requirements.txt
RUN pip install -r /rundir/requirements.txt

# Add the application source code.
ADD . /rundir
#Name the workdir that we need.
WORKDIR /rundir

CMD gunicorn app:app -b 0.0.0.0:8080 -w 1 -t 600
#CMD gunicorn app:app -w 1 -k gevent -t 600