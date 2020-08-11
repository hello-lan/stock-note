#!/bin/bash
# Author:LHQ
# Create Time:Sun 02 Aug 2020 06:45:44 PM CST

code=$1

python main.py add-cashflow -c $code
python main.py add-indicators -c $code
python main.py add-income -c $code

