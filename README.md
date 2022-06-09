# SnakeGame
一个Python &amp; Pygame开发的贪吃蛇小游戏

由[Wotemo](https://www.wotemo.com/)自主编写

### 共有单机版和联机版两种

#### **单机版不能保存得分**

#### **联机版可以保存得分**

注：联机版需要flask框架

本文件夹中的SnakeUsers已安装好虚拟环境和Flask

------

### Flask基本安装方法：
**（联机版看，大神无视)**

1. 打开powershall
2. cd到SnakeUsers文件夹 cd C:\SnakeUsers
3. 构建虚拟环境 py -3 -m venv venv
4. 激活虚拟环境 venv\Scripts\activate
5. 安装Flask pip install Flask
6. 导出 `FLASK_APP` 环境变量 $env:FLASK_APP = "main.py"
7. 运行服务器 flask run --host=0.0.0.0
