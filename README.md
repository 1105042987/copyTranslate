# 使用方法

## 准备

- 在***python***环境中执行:
  
  ```shell
  conda install swig
  pip install pyperclip, PyExecJS, PyHook3
  ```
  
- 把start.bat拷贝到任意一个你觉得方便的地方，比如桌面

- 当确定当前环境可以正常运行`python copyTranslate.py`时，更改start.bat中第一个参数为：

  - **win：**在当前命令行中运行`where python`，将第一个返回值填入
  - **linux：**在当前命令行中运行`which python`，将第一个返回值填入

- 第二个参数更改为copyTranslate.py文件的绝对路径
## 使用

- 双击start.bat

- 如果正常生成了stop.bat，说明脚本正常工作

  - 如果未正常生成，需要在代码文件夹下进入python环境，执行以下指令，查看报错：

    ```shell
    python copyTranslate.py
    ```

- 在该状态中：
  - 每当你按下 “**alt+Q**”，对剪切板进行一次翻译
  - 每当你按下 “**alt+,**” ，在整体翻译与分句翻译之间切换（默认为整体翻译）
  - 每当你按下 “**alt+L**”，翻译语言在中英文之间切换（默认翻译为中文）
  - 快捷键可以在setting.json中设置，请注意务必遵守规则

- 使用结束后，双击生成的stop.bat停止脚本

# 表现

脚本运行中, 每次调用翻译会呈现如下场景
 ![show](./show.png)  