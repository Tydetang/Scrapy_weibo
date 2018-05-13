# Scrapy_weibo
运行：直接python begin.py

运行前需要在cookies.py中添加微博的账号密码

模拟登陆在cookies.py文件中，比较复杂，先在login.sina.com.cn中登陆（其中密码需要进行加密）获得session后再在登陆微博移动端获得cookie，最后在用获得的cookie登陆weibo.cn进行爬取

运行之前要打开mongodb数据库
