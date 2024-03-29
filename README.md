# 使用方法

## 准备

### 方法一 —— 脚本配置：
- 确保python版本为3.7，并且已经安装pip
- 执行以下指令  
  - **注意**，该方法会默认更新pip到最新版本，如果你不想更新，可以参照方法二中的第一条进行环境安装。
  ```python
  python setup.py install
  ```

- 如果已经安装完成，但没有start.bat脚本，可以运行以下指令，不安装环境，只生成当前所激活环境对应的start.bat脚本。
  ```python
  python setup.py
  ```

### 方法二 —— 手动配置：
- 在conda的python环境中按顺序执行以下内容:
  ```shell
  conda install swig
  pip install pyperclip PyExecJS PyHook3
  ```

- 创建start.bat文件，写入内容`start param1 param2`；
  - 其中第一个参数为当：在当前命令行中运行`where python`得到的第一个返回值；
  - 第二个参数为：copyTranslate.py文件所在的绝对路径。

### 方法二错误处理
- 如果在安装PyHook3时报错`Microsoft Visual C++ 14.0 is required`；
  - 访问[Microsoft官网](https://visualstudio.microsoft.com/visual-cpp-build-tools/)或者[第三方网址](https://474b.com/file/1445568-239446865 )下载安装工具并安装文件。

## 使用

- 把start.bat拷贝到任意一个你觉得方便的地方，比如桌面；

- 双击start.bat；

- 如果正常生成了stop.bat，说明脚本正常工作；

  - 如果未正常生成，需要在代码文件夹下进入python环境，执行以下指令，查看报错：

    ```shell
    python copyTranslate.py
    ```

- 在该状态中：
  - 每当你按下 “**ctrl shift Q**”，当剪切板更新时对剪切板进行一次翻译，若未更新则显示上一次内容；
  - 每当你按下 “**ctrl shift A**”，在上次剪切板的基础上，加上该次剪切板的内容进行一次翻译；
  - 快捷键可以在setting.json中设置，请注意务必遵守规则；

- 使用结束后，双击生成的stop.bat停止脚本。

# 表现

脚本运行中，每次调用翻译会呈现如下场景
 ![show](./show.png)  

# 致谢

感谢大佬提供的Google翻译的Token算法，个人在成型的翻译请求API的基础上，只简单增加了大量内容的分句和并行请求功能，用来提高工具的实时性。
