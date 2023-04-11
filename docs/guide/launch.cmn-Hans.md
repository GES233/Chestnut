# 引导应用

## 怎么用

如果是通过命令行接口来启动应用的话：在安装好 Python 环境后，键入 `python -m tinyui launch` 即可。

> **Warning**
> 
> 引导应用最好仅仅在本机部署，因为如果不那样做会导致安全问题，除非运行应用的设备的厂商提供了额外的安全保障。如果要选择这么做的话请确保**你知道你在做什么**。
>
> 我们可能会在后期设置好针对 launch app 的保护。

### 应用场景

主要是面向在本机的部署，换句话说，就是运行应用的设备就是你的设备。

如果选择通过云服务部署，**请确保在引导应用启动期间操作设备的就是你本人或者你信任的人**。

### 使用方法

编写中

## 设计

简而言之，引导应用就是把应用的依赖中安装比较繁琐的那些从命令行转移到了之后出现的网络应用中去。

所以对于引导应用的设计而言，就有以下的要求：

- 依赖的内容（环境以及程序包之类的）~~尽量~~比较少
  - 不要为少而少，应用整体相对易于安装就行
  - 工具类尽量自己写代码
  - 不要有编译以及安装的过程就可以完成启动（对很多使用情景而言，配置环境与部署的过程是必须的，对于萌新来讲，可能确实有点麻烦了）
- 继承自作者之前的网络项目
  - 创建实例的过程（参见 Explore Flask 的「配置」）
  - ~~照葫芦画瓢的~~架构设计
- 报错友好，方便用户检查以及改正

### 启动流程

按照函数的调用来作为线索：

#### `click.command()`

当我们键入 `python -m tinyui` 时，其结果为：

```text
Usage: python -m tinyui [OPTIONS] COMMAND [ARGS]...

  Manager of application.

Options:
  --help  Show this message and exit.

Commands:
  database          Command reated to database(if you are not developer,...
  launch            Launch user to install all dependencies(web solution...
  prerequisite      Command interface for change prerequisite.
  required          Command interface for change required.
  run               Run application.
  set               Configure and set instance.
```

我们只需要在意其中的 `launch` 即可，其他的命令到时再说。

首先，项目的入口为 `tinyui.__main__`，其代码为：

```python
from .infra.command import manage


if __name__ == "__main__":
    manage()

```

一旦在命令行键入/程序被调用时，就会执行 `manage()` 。TinyUI 的命令行选择的是 `click` ，`manage` 也就是一个 `click.Group` ，它包含了一系列的 `click.Command` 以及 `click.Group` 。

`launch` 是在 `tinyui.command.init` 下的一个**命令**。

其有四个选项，分别是 `--dev`、`--pro`、`--host` 以及 `--port`。

前两者是声明应用的环境为开发环境还是生产环境，其实选择哪一点并没有太大的影响，因为引导应用本身就会向用户段暴露大量这台设备的敏感信息（例如设备硬盘的容量、当前 Python 版本，甚至可能允许用户通过浏览器执行命令行或是 Python 代码）。

后两者为部署的地址以及端口，如果在 `0.0.0.0` 启动引导应用，将会抛出警告。因为那意味着其他设备也能够服务器，而在引导应用中，并没有**任何**能够确保你的设备的安全的手段。

在 `launch` 对应的路由函数 `launch_simple_web_app()` 中，使用了 Sanic 的 [动态应用](https://sanic.dev/en/guide/deployment/app-loader.html) 的功能，因为我们使用了带参数的工厂函数。

#### `create_app() -> Sanic`

该函数位于 `tinyui.infra.web.app` 中，参数如下（都需要显式地指定）：

- `mode` 模式，包括 `dev` `test` `prod` 以及 `launch` ，分别是「开发」、「测试」、「生产」以及「引导安装」
- `use_instance` 如果为真，将会从实例文件夹 `/instance` 中读取配置
  - 在 `launch` mode 下，`use_instance` 为 `False`
- `app_id` 应用的 ID ，为了适用于多应用的环境下
  - 来自于之前项目的遗留成果

引导模式下，首先依靠 `create_config()` 生成配置，然后生成 Sanic 实例。

如果 sanic_ext 安装了，将会配置扩展，否则跳过。

然后依次执行 `register_launch`、`register_stream` 以及 `configure_exceptions` 对实例进行相应的操作。

最后返回实例。

#### 注册引导应用

- 注册中间件 —— 添加 `AppConfig` 与 `PageConfig`，用于响应的 HTML 内容的模板的渲染
- 注册蓝图

#### 添加 SSE

SSE 就是 Server-sent event ，一种让服务端可以向客户端**主动**发送消息的技术。

该方面当前暂无设计，等到用到时再作详尽地分析。

#### 配置异常

设定为指定的 Errorhandler
