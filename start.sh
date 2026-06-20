#!/bin/bash

echo "Starting Hermes..."

# если config нет — создаём
if [ ! -f /opt/data/config.yaml ]; then
  echo "Creating config..."
  cp config.example.yaml /opt/data/config.yaml
fi

# если хочешь — можно подменить модель через ENV
if [ ! -z "$MODEL_PROVIDER" ]; then
  sed -i "s/provider:.*/provider: $MODEL_PROVIDER/" /opt/data/config.yaml
fi

if [ ! -z "$MODEL_NAME" ]; then
  sed -i "s/model:.*/model: $MODEL_NAME/" /opt/data/config.yaml
fi

# запуск оригинального entrypoint
bash docker/entrypoint.sh
