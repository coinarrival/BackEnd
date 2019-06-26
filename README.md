# BackEnd

[![Build Status](https://travis-ci.org/coinarrival/BackEnd.svg?branch=master)](https://travis-ci.org/coinarrival/BackEnd)

Back-end project for Coin Arrival

## 环境需求

1. Familiar with Docker

   - docker

1. Unfamiliar with Docker

   - MySQL 5.7
   - python 3

## Usage for Docker familiar User

为了项目部署方案的多样性，你首先需要更改项目的数据库配置文件 `BackEnd/settings.py`:

```python
DATABASES = {
    'default': {
        # ...
        'HOST': 'coin_arrival',  # 与 docker-compose 的数据库服务容器名保持一致
    }
}
```

然后你可以直接通过以下命令启动项目(你当然可以修改 docker 配置文件 `dockerfile` 和 `docker-compose.yml` 来适配自己的需求)：

```bash
# running foreground
docker-compose up # if with -d param it runs background
```

接下来，请通过 `curl` 确保项目已经运行在 8000 端口：

```bash
curl http://localhost:8000/tasks?page=1
# success response data below
# {"data": {"max_pages": 0}, "status_code": 416}* 
```

## Usage for Docker unfamiliar User

### MySQL 数据库配置

启动 MySQL 数据库并在其中创建项目所需数据库

```bash
CREATE DATABASE coin_arrival CHARACTER SET utf8 COLLATE utf8_general_ci;
```

### 修改项目配置文件

- **数据库配置**

    你需要通过修改 `BackEnd/settings.py` 中的数据库配置来帮助项目连接你所希望的数据库

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',   # 数据库引擎
            'NAME': 'coin_arrival',  # 与前一步的数据库名保持一致
            'USER': 'zhangshanfeng',     # 用户名，可以自己创建用户
            'PASSWORD': '******',  # 密码
            'HOST': '127.0.0.1',  # mysql服务所在的主机ip
            'PORT': '3306',         # mysql服务端口
        }
    }
    ```

- **设置允许访问的 IP**

    ```python
    ALLOWED_HOSTS = ['127....']
    ```

- 密钥（务必修改，长度为50的字符串）

    ```python
    SECRET_KEY = '****' # 通信数据加密模式所需的 ASE 加密密钥
    ```

- 关闭调试模式

    ```python
    DEBUG = False
    ENABLE_CRYPTO = False # 设置为 True 开启通信数据加密模式
    ```

### 使用 Django 自带服务器启动

- 脚本启动

    ```bash
    pip install -r requirements.txt # 安装项目依赖，只需运行一次
    bash ./start.sh
    ```
    项目将运行在本地局域网的 8000 端口

- 手动启动

    脚本默认通过 8000 端口启动，你当然可以手动启动，设置成你所希望的端口号：

    ```bash
    pip install -r requirements.txt # 安装项目依赖，只需运行一次
    cd BackEnd
    python manage.py migrate # 更新数据表
    python manage.py makemigrations # 在数据库中应用更新
    python manage.py runserver 0.0.0.0:8000 # 启动项目，端口号可自己修改
    ```

## 使用 apache 服务器部署

*waiting*

### 设置后台管理

```bash
python manage.py createsuperuser
```
输入超级用户的信息即可注册
在`http://projectIP/admin`即可对数据库直接管理
