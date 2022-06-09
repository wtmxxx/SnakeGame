# SnakeGame
一个Python &amp; Pygame开发的贪吃蛇小游戏

### 联机版使用flask框架进行交互

### flask主要用于获取和储存累计得分

------

### Flask基本安装方法：

1. 打开powershall
2. cd到SnakeUsers文件夹 cd C:\SnakeUsers
3. 构建虚拟环境 py -3 -m venv venv
4. 激活虚拟环境 venv\Scripts\activate
5. 安装Flask pip install Flask
6. 导出 `FLASK_APP` 环境变量 $env:FLASK_APP = "main.py"
7. 运行服务器 flask run --host=0.0.0.0
