#!/bin/bash
# Author:LHQ
# Create Time:Sun 02 Aug 2020 06:45:44 PM CST

code=$1

python main.py crawl -d all -c $code

# python main.py crawl -d cashflow -c $code
# python main.py crawl -d indicators -c $code
# python main.py crawl -d income -c $code
# python main.py crawl -d balance -c $code

