# AirCurrency

## Linux环境:

* 更新apt-get
    ```
    apt-get update
    apt-get upgrade
    ```
* 安装git
    ```
    apt-get install git -y
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
    cd /srv
    wget http://download.redis.io/releases/redis-5.0.5.tar.gz
    tar xzf redis-5.0.5.tar.gz
    cd redis-5.0.5
    make

    设置密码 123456
    ```
### 自动化测试项目:

* 拉取项目
    ```
    cd /srv
    git clone https://github.com/yangyuexiong/AirCurrency.git
    ```

* 项目依赖安装
    ```
    pip3 install unittest
    pip3 install requests
    pip3 install shortuuid
    pip3 install prettytable
    pip3 install redis
    pip3 install apscheduler
    pip3 install supervisor
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
* supervisor配置文件与启动
    ```
    cd /etc/supervisor/conf.d
    vim air.conf
    ```
    ```
    [program:air]
    command         = python3 CarryTask.py
    directory       = /srv/AirCurrency/tasks/ApsTasks
    startsecs       = 0
    stopwaitsecs    = 0
    startretries    = 3
    autostart       = true
    autorestart     = true
    stdout_logfile  = /srv/log/aps.log
    stderr_logfile  = /srv/log/aps.err
    user            = root 
    stdout_logfile_maxbytes = 20MB
    stdout_logfile_backups = 20
    redirect_stderr = false
    stopasgroup     = false
    killasgroup     = false
    ```
    ```
    supervisorctl
    start air
    ```

* 拉取最新项目
    ```
    cd /srv 
    sh update_project.sh
    ```

* 更新项目后重启服务
    ```
    cd /srv 
    sh server_start.sh
    ```


### web展示项目:

* 项目依赖
    ```
    pip3 install Flask
    pip3 install redis   
    ```

* 拉取代码
    ```
    git clone https://github.com/yangyuexiong/AirCurrencyWeb.git
    ```

* 启动
    ```
    cd /AirCurrencyWeb
    python3 run.py
    ```

* supervisor配置文件与启动

    ```
    cd /etc/supervisor/conf.d
    vim air_web.conf
    ```
    ```
    [program:air_web]
    command         = python3 run.py
    directory       = /srv/AirCurrencyWeb
    startsecs       = 0
    stopwaitsecs    = 0
    startretries    = 3
    autostart       = true
    autorestart     = true
    stdout_logfile  = /srv/log/air_web.log
    stderr_logfile  = /srv/log/air_web.err
    user            = root 
    stdout_logfile_maxbytes = 20MB
    stdout_logfile_backups = 20
    redirect_stderr = false
    stopasgroup     = false
    killasgroup     = false
    ```
    ```
    supervisorctl
    start air_web
    ```


* 如果使用python3.7+(当前服务器python3.6.8)

    ```
    1.环境隔离
        pip3 install pipenv

    2.启动配置
        vim ~/.bashrc
        export FLASK_ENV='production'

    3.安装依赖
        cd /srv/AirCurrencyWeb
        pipenv install
    
    4.不带web容器启动
        cd /srv/AirCurrencyWeb
        pipenv shell
        pipenv python3 run.py
    
    ```
