# 项目的架构设计

根据 ChatGPT 提供的信息：

> Clean Architecture 是由 Robert C. Martin 提出的一种软件架构设计理念，主要目的是实现代码的可维护性、可扩展性、可测试性等。它将软件系统分为多个层次，每个层次都有其独立的职责和目的。
>
> Clean Architecture 中最核心的概念是“依赖倒置原则”（Dependency Inversion Principle），该原则要求高层模块不应该依赖于底层模块，而是应该依赖于抽象接口。这意味着具体实现应该依赖于抽象定义，而不是反过来。通过这种方式，可以实现代码的可测试性、松耦合性等。
>
> Clean Architecture 的整体结构主要包括以下几个层次：
>
> 1.  实体层（Entities）：定义业务实体和业务规则。
>
> 2.  用例层（Use Cases）：实现业务用例并协调各个实体完成任务。
>
> 3.  接口适配层（Interface Adapters）：将用例层输出的数据适配为各种不同的外部接口，比如数据库、用户界面等。
>
> 4.  框架和驱动层（Frameworks and Drivers）：提供一些通用的技术设施，比如数据库、Web框架等。
>
> 这些层次的目的是为了实现解耦和高内聚，每个层次的变更只会对本层次的代码造成影响，不会对其他层次造成影响，从而提高代码的可维护性和可扩展性。

但是，Chestnut 并不算是一个严格遵守了整洁架构的应用，我们对各个包的安排如下：

- `root`
  - `adapter` 适配器
  - `application` 应用本体，我为了将应用内外分隔开，将 `Domain` 和 `Usecase` 整合到了一起
    - `{name by context}`
    - `core`
      - `domain`
        - `entity` `DomainModel` 以及 `DomainService`
        - `repo` 即 Repository
      - `usecase` 用例
      - `dto` Data Transform Object，用例输入输出的对象
      - `exceptions` 此处的异常
  - `infra` 即 `Infrastructure` ，基础设施
    - `deps` 即 `dependencies` ，依赖项
      - `service` 将依赖项包装为服务供外界使用
      - `settings` 相关配置（可选）
    - `helpers` 自写的一些常用的工具类/函数/对象
      - `config` 提供了一些对字典的 `__setattr__` 以及 `__getattr__` 方法的类
    - 还有一些基础的框架，例如命令行、网络框架以及魔改的日志

关于测试代码的内容为：

- `/tests` 
  - `/infra` 对应着基建以及基建+应用
  - `/app` 对应着应用

我们计划在前端也采用这种架构。
