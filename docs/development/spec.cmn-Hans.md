# 规范

关于 TinyUI 项目的规范。

## 开发环境

Windows 11 下的 VSCode 。

## Git

> _Add some segment._

略。

### 工作流

### 提交信息

## 文档约定

### 命名

英文文档：`{name}.md`

其他语言的文档：`{名字}.{语言代号}.md` ，如果项目为单一语言是可以为 `{name}.md` 。

当文档作为模板时，其名字为：`{原来的名字}-sample`/`{原来的名字}-template`

关于图片：**统一**在文件项目根目录下的 `/assets` 文件夹。

### 关于 `README`

其参考了 [standard-readme](https://github.com/RichardLitt/standard-readme) 。

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
# 单独写一行注释声明
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
