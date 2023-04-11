# 关于文档

## 文档本身

针对文档本身的一些约束组成了业务逻辑，因此我们计划将文档作为领域模型。

## 文档读取

一种网页端读取给定目录文档的功能。

### 为什么有这个

考虑到部分用户可能有点难以查阅在不同目录下的文档，故把其嵌入了 WebUI 中。

在浏览器中的目录：

- `/docs` 所有文档的索引
- `/docs/<RepoName:Optional>/<lang:Optional>/Any`
  - `RepoName` 是仓库的目录
  - `<lang>` 附带语言的目录（在这多语言目录下很有用）
  - 其中 `Any` 是文档相对于**其**根目录的相对目录

例子如下：

- 单一仓库单一语言
  - 在本地：`/docs/example/example.md`
  - 在浏览器：`/docs/example/example`
- 多仓库多语言
  - 本地 `<Repo1Path>/Repo1` 下有文档，其中我们要读取 `/test/q.md` 以及 `/test/a.zh.md`
  - 在浏览器上为 `/docs/Repo1/en/test/q` 以及 `/docs/Repo1/cmn/test/a`

对文件的一些约束：参见[约定](/docs/development/spec.cmn-Hans.md)。

### 如何实现

大致分为两步：

- 先从系统目录中读取文档目录以及**所有的**文档本体（不包括 `/assets` 下的内容）至数据库并建立索引
- 倒时从数据库/系统目录中装载对应内容至浏览器

也就是需要两个 `Adapter` 来实现 `Repository`：

- `DAO` 与数据库
- `FileLoader` 与文件

在实现中，我们将其变成针对 `DocRepo/DocMetaRepo` 的抽象。

#### 为什么要有单独的 `Metadata` ？

考虑到某些文件内容过大，在通过 `FileLoader` 装载后对文件的处理过于麻烦。
