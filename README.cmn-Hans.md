# 【施工中】栗子 🌰

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black) [![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

[English](/README.md) [繁體中文](/README.cmn-Hant.md)

基于 [Sanic](https://github.com/sanic-org/sanic) 以及 [AppRun](https://apprun.js.org) 构建的演示以及使用 AI 项目的脚手架。

灵感来自于 [AUTOMATIC1111's WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 及其丰富的生态；以及更早地，之前采用编程方法所完成、而且能够随机生成不同结果以便其他同学借鉴~~抄袭~~的大作业。

## TOC

- [特点](#特点)
- [第一步](#第一步)
- [使用方法](#使用方法)
  - [安装以及运行](#安装以及运行)
  - [依赖项](#依赖项)
  - [目前存在的功能](#目前存在的功能)
    - [面向开发者](#面向开发者)
    - [面向使用者](#面向使用者)
- [鸣谢](#鸣谢)
- [开发者名单](#开发者名单)

## 特点

- 领域驱动设计 + 整洁架构 => 便于重构以及拓展
- 更少的命令行参数以及提供了多种启动方法
- 对外人（指不懂相关技术的人）友好

## 第一步

配置好环境、下载代码以及运行引导应用。

```bash
python virtualenv venv python=3.10
source venv/bin/activate
git clone https://github.com/GES233/Chestnut.git
python -m pip install -r requirements_basic.txt
python -m chestnut launch
```

在命令行出现相关信息时，就说明引导应用成功运行。
然后在浏览器打开 http://127.0.0.1:6699 ，跟随网页的内容以及提示来进行下一步操作。

## 使用方法

### 安装以及运行

需要 Git 、 Python 以及 OpenSSL 。

如果您不知道怎么安装这些的话，参见 [面向萌新的运行环境的搭建](/docs/guide/newbie.cmn-Hans.md#安装前) 。

如果您知道的话，就不用看了，里边的内容相当基础，如果您有经验的话可能显得有点浪费时间。简而言之就是编程相关内容的基础知识 + 常见的坑 + 踩坑后如何爬出来。

### 依赖项

Chestnut 基于 Python 运行，如果用户的环境里有 Node.js 的话可能会涉及到 Javascript/Typescript 的相关内容。所以这里着重介绍 Python 的依赖项，至于其他的部分，因其主要是面向开发者的，所以在会在 [文档](/docs) 里讲到。

- **Python**
  - WebUI（引导应用）:  *最最基本的，如果想要顺利运行的话一定要有。*
    - [`click`](https://palletsprojects.com/p/click/) 实现项目的命令行接口。
    - [`sanic`](https://sanic.dev/) 服务器以及网络框架。
    - [`jinja_2`](https://palletsprojects.com/p/jinja/) 生成要返回到浏览器的 HTML 的模板库。
    - [`pydantic`](https://pydantic.dev/) 序列化以及反序列化（人话：应用内部以及外部接口的“翻译”），
    - [`tomli`](https://github.com/hukkin/tomli) 对 `*.toml` 配置文件的解析。如果是 Python 3.11 以上，不再需要额外安装，因为在那个版本已经作为标准库的一员（`tomllib`）了。
    - [`aiosqlite`](https://aiosqlite.omnilib.dev) 负责对硬盘上的数据库的读取。
    - [`SQLAlchemy`](https://www.sqlalchemy.org) 用 Python 对象而非 SQL 语句来实现对数据库的操作。
    - [`Alembic`](https://alembic.sqlalchemy.org/) 和 SQLAlchemy 高度耦合的用于实现数据库迁移的库。
  - WebUI（为了安全需要可选[^optional]）:
    - [`ecdsa`](https://github.com/tlsfuzzer/python-ecdsa) 椭圆曲线加密的相关库。如果仅仅是本地部署，不是必需安装的。
  - WebUI（为了展现文档以及美化内容可选）:
    - [`mistune`](https://mistune.lepture.com/) 将 Markdown 渲染成 HTML（服务端渲染下）。
    - [`Pygments`](https://https://pygments.org/) 代码高亮工具（确实不是必需的，不过为了代码显示起来好看些，还是被放在了 [Basic requirements](/requirements_basic.txt) 里）。
  - WebUI（主应用）:
    - 上者所有（仅包括必需以及 `ecdsa`）。
    - [`sanic_ext`](https://sanic.dev/en/plugins/sanic-ext/getting-started.html) Sanic 的官方插件，我们主要要用到 DI （依赖注入）、 template （针对 Jinja2 的浅封装[^templating]）以及 OpenAI （API 文档）等等。
  - 模型: _具体需要哪些取决于应用，因此未在 `requirements` 中体现出来。_
    - [`torch`](https://pytorch.org) 因为项目的目标是演示**机器学习**项目，所以需要 `PyTorch` 。
    - [`safetensors`](https://github.com/huggingface/safetensors) 装载/保存 `*.safetensors` 模型。
- 装饰美化
  - [**PicoCSS**](https://picocss.com) *这个被放在模型里了。*
- 前端[不是必须的]
  - [**Node**](https://nodejs.org): 如果安装了，在 `/webapp` 内的前端项目会重新编译打包，如果你要二次开发是必须的。
  - [**Tailwind CSS**](https://tailwindcss.com) 美化，比 PicoCSS 复杂得多但是可定制性更强。
  - [**AppRun**](https://apprun.js.org) 实现单页面应用。
  - [**Vite**](https://vitejs.dev/) 打包应用。

[^optional]: 这里「可选」的意思是，就算安装失败了也没事，没有必要非要安装，下文同理。

[^templating]: 其实这个功能用不大到，因为我们计划在主应用的后端采用 API+SSE 为返回的形式。但是，如果未安装 Node ，可能也就会用到。

### 目前存在的功能

#### 面向开发者

如果你想通过 Chestnut 来实现你的项目的话，可以看下 [开发者说的话](/docs/development/development.cmn-Hans.md) 。

规范参见 [规范](/docs/development/spec.cmn-Hans.md) 。

#### 面向使用者

暂无。

## 鸣谢

~~写完再说。~~

## 开发者名单

目前仅有 [我自己](https://github.com/GES233) 。
