#!/bin/bash
# Author:LHQ
# Create Time:Sat 18 Jul 2020 10:42:32 AM CST

gunicorn -b 0.0.0.0:8000 wsgi:app