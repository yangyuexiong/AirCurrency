# AirCurrency

## Linux:


* 更新apt-get
    ```
    apt-get update
    apt-get upgrade
    ```
* 安装git
    ```
    apt-get install git -y
    ```
* 拉取项目
    ```
    git clone https://github.com/yangyuexiong/AirCurrency.git
    ```
* 安装pip3
    ```
    apt install python3-pip
    ```
* 配置python3与pip3
    ```
    vim ~/.bashrc
    ```
    ```
    # python path 
    alias python='/usr/bin/python3'
    alias python3='/usr/bin/python3'

    # pip path
    alias pip3='/usr/bin/pip3'
    ```
    ```
    source ~/.bashrc
    ```
* 安装 redis
    ```
    wget http://download.redis.io/releases/redis-5.0.5.tar.gz
    tar xzf redis-5.0.5.tar.gz
    cd redis-5.0.5
    make
    ```

* 项目依赖
    ```
    pip3 install unittest
    pip3 install requests
    pip3 install shortuuid
    pip3 install prettytable
    pip3 install redis

    ```
* 运行
    ```
    # 默认执行全部用例
    python3 run.py

    # 单个用例执行
    python3 run.py 交易所名称    # python3 run.py okex
    ```

* 定时任务
    ```
    cd /AirCurrency/tasks/ApsTasks

    python3 CarryTask.py # 默认执行所有用例
    ```
* 报告目录
    ```
    /AirCurrency/reports
    ```