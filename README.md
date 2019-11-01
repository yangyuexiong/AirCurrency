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
    pip3 install shortuuid
    pip3 install prettytable
    pip3 install redis

    ```