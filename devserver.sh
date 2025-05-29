#!/bin/sh
source .venv/bin/activate
export NAME=Longstagram
export DATABASE_URL=mysql+pymysql://root:@localhost:3306/longstagram
python -m flask --app main run --debug