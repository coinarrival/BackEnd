# BackEnd

[![Build Status](https://travis-ci.org/coinarrival/BackEnd.svg?branch=master)](https://travis-ci.org/coinarrival/BackEnd)

Back-end project for Coin Arrival

## 环境需求
- MySQL 5.7
- python 3

## mysql数据库配置

```bash
CREATE DATABASE coin_arrival;
```



## 修改配置文件`BackEnd/settings.py`

- 数据库配置

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # 数据库引擎
        'NAME': 'coin_arrival',  # 数据库名，先前创建的
        'USER': 'zhangshanfeng',     # 用户名，可以自己创建用户
        'PASSWORD': '******',  # 密码
        'HOST': '127.0.0.1',  # mysql服务所在的主机ip
        'PORT': '3306',         # mysql服务端口
    }
}
```

- **密钥（务必修改，50长度的字符串）**

```python
SECRET_KEY = '****'
```

- 关闭调试模式

```python
DEBUG = False
ENABLE_CRYPTO = True
```

- 设置ip仅服务端可以访问

```python
ALLOWED_HOSTS = ['127....']
```



## 安装（测试方案，使用django自带服务器）

```bash
pip install -r requirements.txt
cd BackEnd
python manage.py migrate
python manage.py makemigrations account_info
python manage.py runserver 0.0.0.0:8000
```
默认8000端口，也可以修改

## 安装（正式，使用apache服务器）

```
TODO...
```



## 设置后台管理
```bash
python manage.py createsuperuser
```
输入超级用户的信息即可注册
在127.0.0.1:8000/admin即可对数据库直接管理

```python
SECRET_KEY = '****'
```