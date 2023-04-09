# 前端的架构设计

## 引导应用

Jinja2 的服务端渲染到 HTML + PicoCSS 美化 + 简单的 JS （在 /public/plain/...）。

## 主应用

计划采用 AppRun 实现 SPA 。
也有使用 Jinja + PicoCSS + mistinue 的计划（在用户未安装 Node 时选择）。

## 报错

对于通过后端的请求，主要是使用我们编写的继承 Sanic 的 Errorhandler 的一个类，它：

- `/api` 下返回自带的 JSONRenderer
- 其他情况下返回网页，是基于 PicoCSS + 魔改版 Sanic 报错界面搭建的
