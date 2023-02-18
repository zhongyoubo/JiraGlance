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


