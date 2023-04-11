# 开发

> **Note**
>
> 这是项目的设计文档而非面向新人的教程，所以里边部分内容可能会「超纲」，敬请留意。

## 向 TinyUI 推送分支

参见 [为 TinyUI 添砖加瓦](/docs/development/) 目录。

## 添加你的应用

### 作为代码仓库的应用

...

### 作为可被导入的 Python 包

...

### 更新应用

复制自己的分支，之后：

- [`/tinyui/infra/web/settings/__init__.py`](/tinyui/infra/web/settings/__init__.py): `create_app_config()` => 你起的名字[开发模式下]
- [`/tinyui/infra/web/settings/__init__.py`](/tinyui/infra/web/settings/__init__.py): `create_app_config()` => 你起的名字[测试模式下]
- [`/tinyui/infra/web/settings/__init__.py`](/tinyui/infra/web/settings/__init__.py): `create_app_config()` => 你起的名字
- [`/tinyui/infra/web/settings/__init__.py`](/tinyui/infra/web/settings/__init__.py): `create_app_config()` => 你的介绍
- [`/tinyui/infra/web/settings/__init__.py`](/tinyui/infra/web/settings/__init__.py): `create_app_config()` +<- 更多
  - 如果你想知道怎么实现的话，请查看 [`AppConfig`](/tinyui/infra/helpers/config/app.py) 的代码
  - 如果你想的话移除创建应用实例的函数 [`createappconfig()`](/tinyui/infra/helpers/config/inst/render.py) 或者令其返回 `""`
- [`/tinyui/infra/web/settings/__init__.py`](/tinyui/infra/web/settings/__init__.py): `create_config()` => 如果要的话也把 `prefix_` 改一下
- [`/tinyui/infra/web/settings/__init__.py`](/tinyui/infra/web/settings/__init__.py): `create_config()` => 你的引导应用的名字
- [`/tinyui/infra/helpers/link.py`](/tinyui/infra/helpers/link.py): `APP_LINK` => 你的代码仓库/网站链接
- [`/tinyui/infra/cli/init.py`](/tinyui/infra/cli/init.py): `configure_app()` => 更新对应的名字以及介绍
- [`/tinyui/application`](/tinyui/application/) & [`/tinyui/adapter`](/tinyui/adapter/) -> 在这里添加你的代码，并且将其注册到应用上
- [`/tinyui/infra/deps/database/settings.py`](/tinyui/infra/deps/database/settings.py): `database_dev` & `database_prod` => 你起的名字
- [`/tinyui`](/tinyui/) => 你起的名字
- [`/alembic.ini`](/alembic.ini): script_location & sqlalchemy.url => 对应的修改到你的包名以及你起的数据库的名
- [`/tests`](/tests/) -> 如果 IDE 没有工作的话，那么手动修改吧，顺便还有每个 module 的注释
- [`/public/launch/template/`](/public/launch/template/) -> 加上你的模板
- [`/public/launch/static`](/public/launch/static/) -> 加上你的脚本
- [`/webapp`](/webapp/) -> 把你的前端代码加进去（细节等后面再加上）
  - 如果不精通前端的话，也可以：
    - 将 [`AppConfig.build`](/tinyui/infra/helpers/config/app.py) 改为 `False`
    - 选择在 [plain](/tinyui/adapter/plain/web/) 内填充路由函数的代码（简单地导入几个 `Usecase` 再使用即可），在 [模板](/public/plain/template/nonode/) 内填充对应的模板
- [`README.md`](/README.md) & [`/docs`](/docs/) -> 你的文档
