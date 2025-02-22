#!/bin/bash

service redis-server start

python publisher_app.py &

python subscriber.py