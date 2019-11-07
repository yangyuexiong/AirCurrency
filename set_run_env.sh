#!/usr/bin/env bash



set_dev(){
    if [ $1 == "mac" ]
    then
    sed -i "" 's/export RUN_ENV=pro/export RUN_ENV=dev/g' /Users/yangyuexiong/.bash_profile
    source /Users/yangyuexiong/.bash_profile
    elif [ $1 == "linux" ]
    then
    echo 'set linux profile pro to dev'
    else
    echo "错误参数"
    fi
}

set_pro(){
    if [ $1 == "mac" ]
    then
    sed -i "" 's/export RUN_ENV=dev/export RUN_ENV=pro/g' /Users/yangyuexiong/.bash_profile
    source /Users/yangyuexiong/.bash_profile
    elif [ $1 == "linux" ]
    then
    echo 'set linux profile dev to pro'
    else
    echo "错误参数"
    fi
}


if [ $1 == "mac" ] && [ $2 == "dev" ]
    then
    echo "mac dev"
    set_dev mac

    elif [ $1 == "mac" ] && [ $2 == "pro" ]
    then
    echo "mac pro"
    set_pro mac

    elif [ $1 == "linux" ] && [ $2 == "dev" ]
    then
    echo "linux dev"
    set_dev linux

    elif [ $1 == "linux" ] && [ $2 == "pro" ]
    then
    echo "linux pro"
    set_pro linux

    else
    echo "错误参数"
fi



