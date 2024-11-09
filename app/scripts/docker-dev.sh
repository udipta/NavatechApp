#!/bin/bash

set -e
set -x

echo "127.0.0.1 dev-api.navatech.ai  # Dummy API for CORS" | sudo tee -a /etc/hosts
echo "127.0.0.1 dev.navatech.ai      # Navatech Org" | sudo tee -a /etc/hosts

# generate files from template
cp ./app/.env.docker.template ./app/.env.docker
