#!/usr/bin/sh

set -e

docker build -t covidnet_integration --file Dockerfile .
