#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM python:latest

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

#RUN echo 'Defaults env_keep="http_proxy"' > /etc/sudoers
#RUN echo 'Defaults env_keep="https_proxy"' > /etc/sudoers


# extra dependencies (over what buildpack-deps already includes)
RUN apt-get update && apt-get install -y --no-install-recommends \
		tk-dev
RUN apt-get install nano
RUN rm -rf /var/lib/apt/lists/*

#ENV GPG_KEY 97FC712E4C024BBEA48A61ED3A5CA953F73C700D
ENV PYTHON_VERSION 3.5.7
#RUN wget https://bootstrap.pypa.io/get-pip.py
RUN /usr/local/bin/python3 -m pip install lxml requests redis

WORKDIR /

COPY iaai.py /iaai.py
COPY start.sh /start.sh
RUN chmod 777 /start.sh

CMD [ "./start.sh" ]

