#!/bin/bash
xargs -a apt-requirements.txt apt-get install -y
pip3 install -r requirements.txt
