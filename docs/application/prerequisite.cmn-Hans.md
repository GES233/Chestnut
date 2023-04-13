# 关于依赖项的设计

## 用途

简而言之，依赖项（`Prerequisite/ReauiredItem`）包装了对运行 Chestnut 内某些应用的所必需的对象。

## 要用到的环境

在 Chestnut 中，有以下的环境需要涉及到依赖项：

- 在 launch 下检查当前运行环境中是否存在特定依赖项
- 在用户端（CLI/WebUI）梳理依赖项、依赖程度以及安装方法
- （作为其他环境的上游）提供并封装依赖项 [可能不需要]

其对应着 `PrerequisiteItem` 以及 `RequiredItem` 的用例：

- `CheckUsecase` in `LaunchContext`
  - 检查环境内所有的依赖项的存在情况并且保存到数据库
- `DisplayUsecase` in [All]
  - 将依赖项的信息展现出来，内容由开发者自定义，也可以被用户所修改
- `SupplyUsecase` in [All]
  - 检查依赖项的相关关系并且对**依赖程度**进行推断
- `UpdateUsecase` in [All]
  - 重新检查依赖项的存在情况，更新数据库

## 相对应的领域模型

### `RequiredItem`

简而言之，就是领域模型**内部**所必需的依赖项。

为了和与领域模型无关的基础设施的依赖项（`Dependency`）区分开来，采用了这个名称，原因如下：

- 直译为「先决条件」，应用内大多数的业务逻辑离不开它，但相比处于基础设施层的 `Dependency` 而言有一层潜封装，故此在所依赖的对象并不存在的情况下，应用内的部分业务逻辑是可以运行的（引导应用首次启动是的预设值是所有的 `Prerequisite` （见下文）都不存在）
- `DependentItem` 字母更长（虽然也就长了一点点）

它能够：

- 能够保存一些信息，包括：
  - 名字（作者起的别名）
  - 对项目的依赖程度（决定于所有的 `Pipeline` 所需要的 `Prerequisite` 的集合）
    - `Required when install` 启动应用时必需的
      - 例如某个被用到的 Python 包
    - `Required but pluggable` 运行时必需但是不具备唯一性的
      - 例如模型权重
    - `Required to facilitate development` 开发时必需的
      - 例如测试工具
    - `Optional for appearance` 为改善外观可以选择的
    - `Optional for performance` 为提高性能可以选择的
    - `Optional to facilitate development` 开发时可以选择的
    - `Optional for specific cases` 其他特定用途
    - `Useless` 不需要
  - 类型 **<mark>和 Python 的类型没有关系</mark>**
    - `PythonObject`：Python 对象
    - `PythonModule`： Python 包
    - `Command`：命令（能够通过命令调用的程序）
    - `Program`：程序
    - `File`：存放在磁盘上的文件（某一个或某一类）
    - ...
  - 简介（一句话描述 + 链接/作者链接 + 安装方法 + 使用方法 etc.）
  - 安装方法
    - `AutomaticInstallation` 例如 Python 包或下载指定的文件
    - `MannualInstallation` 例如安装并配置复杂的应用
    - 一般的讲，它们间并不是界限分明的
  - 获取链接 或 调用/获取的路径
  - 用于校验的信息（如果是代码模块则会是调用以及检查版本的指令；如果是文件则会是散列值（当对唯一性有要求时）、后缀名或是目录或者加载后的 Python 对象的类型；如果是环境变量则是其本身）
- 能够检查所对应的组件/库/框架/文件/环境变量是否存在以及可用性
- 将该组件/库/框架/文件/环境变量的对象以某种形式封装来方便调用（可有多个以便不同的 `Manipulator` 引用）

考虑到部分 `Prerequisite` 的装载过程耗时以及对资源的占用较大（例如需要较长时间以加载的程序或是几个在 AI 任务中动辄数 G 的权重文件），实现需要对上下文进行设计。

### `PrerequisiteItem`

当前环境存在的依赖项，是 `RequiedItem` 的子集。

在应用中由 `RequiredItem` 根据当前的环境生成（in `CheckUsecase`）。

包含以下内容：

- 名字（和 `PrerequisiteItem` 一样）
- 展示组件/库/框架/文件/环境变量的状态 —— 作为一个承载这些内容的容器
  - `Exist`
  - `NotConfigured`
- 唯一值（可选）
- 调用方法（和 `PrerequisiteItem` 一样）

## 例子

我们想要包括两个例子来演示这套机制：

- `Node.js`
- `sanic_ext`
