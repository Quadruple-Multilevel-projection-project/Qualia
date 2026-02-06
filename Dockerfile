FROM python:3.11-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends nodejs npm \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY core ./core
COPY bridge ./bridge
COPY manifest ./manifest

RUN cd bridge && npm install

CMD ["python", "core/amne_full_intellect.py", "--validate-only"]
