建立Project Folder
    如JiraGlance，并用vscode打开
建立python虚拟环境
    vscode：终端->新终端->执行：python -m venv .env
选择python虚拟环境解释器
    vscode：查看->命令面板->输入选择：Python：Select Interpreter 选择解析器,选择后面带有（'.env':venv）的解析器;
    左下角显示Python 版本（'.env':venv)
安装包到虚拟环境
    以安装flask为例
    vscode：终端->新建终端（显示目录前带有（.env））->执行：pip install flask，终端中显示Successfully表示安装成功

建立Project files
    在新建立的文件中 建立 app.py 文件

运行测试
    vscode：终端->新建终端（显示目录前带有（.env））->执行：python -m flask run

将代码部署到linux服务器：
    默认情况下，Flask内置的开发服务器会监听本地机的5000端口，你可以使用127.0.0.1:5000或localhost:5000访问程序
    app.run()方法运行服务器应用，默认是只能在本机访问的！！！如果需要在其他机器上访问，需要修改为：app.run(host='0.0.0.0')
   
    app.py添加#!/usr/bin/env python3.6，用python执行脚本
    
    添加启动脚本server_run.sh，bash server_run.sh用于启动或者重启应用

