#!/bin/bash

./manage.py migrate;
if [ $DEBUG == 0 ]
then
    uvicorn --host 0.0.0.0 --port 5804 api.asgi:application;
else
    ./manage.py runserver 0.0.0.0:5804;
fi
