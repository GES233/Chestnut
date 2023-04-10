# 规范

关于 TinyUI 项目的规范。

## 开发环境

Windows 11 下的 VSCode 。

## Git

> _Add some segment._

需要等到项目具备一定的完成度再讨论。

### 工作流

### 提交信息

## 文档约定

### 命名

英文文档：`{name}.md`

其他语言的文档：`{名字}.{语言代号}.md` ，如果项目仅有单一语言时也可以为 `{name}.md` 。

> **Note**
>
> 关于单一语言文档：原则上**不建议**非英文的省略掉，因为一旦未在文件名中检测出语言，`TinyUI` 的缺省值就是英文。

当文档作为模板时，其名字为：`{原来的名字}-sample`/`{原来的名字}-template`

关于图片：**统一**在文件项目根目录下的 `/assets` 文件夹。

### 关于 `README`

其参考了 [standard-readme](https://github.com/RichardLitt/standard-readme) ，目前 `TinyUI` 的格式如下：

- 标题
  - 大写
- 目录前
  - 提示以及警告(可选)
  - 项目简介
  - 徽章
  - 其他语言
  - 简短的描述
- TOC
- 正文

## 环境

我们将项目分为开发环境（`dev`）、测试环境（`test`）以及生产环境（`pro`/`prod`）。

### 实例

项目有一个实例文件夹 `/instance` ，`python -m tinyui set` 命令能够在初始化应用的同时创建这个文件夹。

### 关于 Docker

## 代码格式与编码约定

### 后端

TinyUI 的服务端不管是基建还是应用内部均由 Python 写成，所以本节内容主要针对 Python 。

### Formatter

我们选择 [Black formatter](https://github.com/psf/black) 来约束代码格式。

### 导入包

我们希望在以下情况，尽量使用**相对导入**：

- 导入的是应用程序内部的包
  - 在本项目中，「内部」指的是 `tinyui` 这个包的内部
  - 不包括插件

在其他情况，尽量使用绝对导入。

在包中，导入其他包的排列顺序为：

```python
# Python 标准库
import os, sys
import dataclasses
# 先 `import ...` 再 `from ... import ...`
from pathlib import Path
# 关于类型注解的库放在本节的最后
import typing as t

# 空一行，然后是第三方的库
import email_validator
from pydantic import BaseModel

# 再空一行，然后是应用内的相对导入
# 其排列顺序为，先近后远，先短后长，如果一样那么按照字母排序或代码的列数
from .. import cat as meow
from ...foo import bar
from ...foo.bar.alg import lsp


# 如果要导入的包是用应用属性的话（e.g. 下属的蓝图）
# 需要再单独写一行注释声明
from .index import index_bp
from .docs import docs_bp


...
```

在一些特殊情况下，为了避免循环导入，可以先写源码再导入其他库以该内容为输入的其他的应用，比方说：

```python
# base.py
from . import a


a_instance = a()


# 导入用到 a 的其他包
from .b import b_inst
from .c import c_inst
```

其他情况需要后续讨论。

### 类型注解

由于 TinyUI 运行时需要类型标注，因此我们推荐在源码中尽量多的使用到类型注解。

## 前端

可能会参考 [Project Guidelines](https://github.com/elsewhencode/project-guidelines) 的相关内容。

### Javascript

### Typescript

前端的 SPA 采用 AppRun 框架，而 AppRun 可以同时选择 Typescript 以及 Javascript ，为了避免发生后来看不懂自己之前写的代码的情况发生，我们更倾向于针对那些需要打包的代码（`/webapp` 内）选择 Typescript。

#### 代码指导

略。
