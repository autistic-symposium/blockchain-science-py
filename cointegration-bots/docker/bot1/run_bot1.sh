#!/bin/sh

# these files should be in .gitignore
cp -r src ./docker/bot1/src
cp -r requirements.txt ./docker/bot1/requirements.txt
cp -r .env ./docker/bot1/.env
cp -r setup.py ./docker/bot1/setup.py
cp -r Makefile ./docker/bot1/Makefile


make build_bot1 && make up_bot1


