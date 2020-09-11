# StockNote

股票研究笔记工具



## Table of Contents

  - [Background](#background)
  - [Project Structure](#project-structure)
  - [Install](#install)
  - [Usage](#usage)



## Background

A股上市公司的分析框架，包括财务数据、基本面和估值等。本项目使用python3语言开发，采用了flask框架，启动后可在浏览器打开使用。



## Project Structure

```
stock-note
├── readme.md
├── requirments.txt
├── run.sh           // 服务启动脚本
├── scripts          // 数据脚本，主要是一些爬虫
│   ├── crawlers     // 爬虫
│   :
│   ├── main.py      // script的命令入口
│   └── load_stockdata.sh
└── stocknote            // flask应用
    ├── __init__.py      // app
    ├── settings.py         // flask配置文件
    ├── extensions.py       // flask的一些扩展插件
    ├── blueprints          // controllers
    ├── models              // orm模型定义
    ├── services    
    ├── static
    ├── templates   
    └── utils

```



## Install

```bash
pip3 install -r requirements.txt
```



## Usage

linux终端中执行

```
bash run.sh
```

然后浏览器打打开 localhost:8000即可


首次部署，先初始化数据库(建表)

```
flask initdb
```

然后添加某只股票(以002003为例)的财务数据，在另一个终端中执行

```
$ cd scripts
$ bash load_stockdata.sh 002003
```
