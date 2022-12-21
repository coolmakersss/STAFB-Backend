# STAFB-Backend
For BUAA DB Homework

## 运行方式

建立虚拟环境

```sh
virtualenv venv
```

进入虚拟环境
```sh
source venv/bin/activate
```

安装依赖
```sh
pip3 install -r requirements.txt
```

获取 config.yaml 后，运行服务器
```sh
python3 manage.py runserver
```



## 部署命令
```sh
sudo docker build -t stafb-backend:test .
sudo docker ps
sudo docker stop "CONTAINER ID"
sudo docker run  -v ~/photo-set:/app/photo-set -d -p 8100:8000 "stafb-backend:test"
```