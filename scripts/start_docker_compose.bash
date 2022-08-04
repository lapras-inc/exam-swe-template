#!/usr/bin/bash -eu

service_name="$1"
condition="$2"

start_time="$(date -u +%FT%T)"

docker-compose up -d

while [ "$(docker-compose logs --no-color --timestamp | awk '$1=="'"$service_name"'"&&$3>="'"$start_time"'"' | grep -c "$condition")" -eq 0 ]; do
  echo "Waiting for: service_name=$service_name, condition=$condition"
  sleep 10

  if [ "$(docker-compose ps | grep -Ec "$service_name.+Up")" -eq 0 ]
  then
    echo "Failed to start."
    docker-compose logs
    docker-compose ps
    exit 1
  fi
done

echo "Ready."
sleep 10
