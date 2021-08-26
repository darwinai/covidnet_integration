FROM fnndsc/ubuntu-python3:18.04

ENV APPROOT="/usr/src/covidnet_integration"
RUN mkdir $APPROOT
ENV DEBIAN_FRONTEND=noninteractive
COPY ["requirements.txt", "apt-requirements.txt", "${APPROOT}/"]

WORKDIR $APPROOT

RUN apt-get update \
  && xargs -a apt-requirements.txt apt-get install -y \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade pip \
  && pip install -r requirements.txt

COPY ["upload_swift_notify_cube.py", "${APPROOT}"]

CMD ["upload_swift_notify_cube.py", "--help"]
