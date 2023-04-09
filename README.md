# [WIP] TinyUI

> **Warning**
> 
> This project is still in progress and may be deprecated at any time.

[简体中文](/README.cmn-Hans.md) [繁體中文](/README.zh-cmn-Hant.md)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A scaffold built with Sanic and AppRun. 

## TOC

- [Feature](#feature)
- [Getting Start](#getting-start)
- [Usage](#usage)
  - [Install and running](#install-and-running)
  - [Dependencies](#dependencies)
- [Contributors](#contributors)
- [Thanks](#thanks)

## Feature

- DDD + Clean Architecture => obey Open-Close Principle.
- Fewer params in command => easy to read and operate

## Getting Start

Download the source code and run launch app.

```bash
python virtualenv venv python=3.10
source venv/bin/activate
git clone https://github.com/GES233/TinyUI.git
python -m pip install -r requirements_basic.txt
python -m tinyui launch
```

Then, open `http://127.0.0.1:6699` in browser and follow it to install.

## Usage

### Install and running

Before running, you need install Python and Git.

### Dependencies

- **Python**
  - WebUI(Launch):
    - [`click`](https://palletsprojects.com/p/click/) command
    - [`sanic`](https://sanic.dev/) server and framework
    - [`jinja_2`](https://palletsprojects.com/p/jinja/) template to render HTML file
    - [`pydantic`](https://pydantic.dev/) serialization & deserialization
    - [`tomli`](https://github.com/hukkin/tomli) (less than Python 3.11)
    - [`aiosqlite`](https://aiosqlite.omnilib.dev) for Database
    - [`SQLAlchemy`](https://www.sqlalchemy.org) ORM(bind Python object with database)
    - [`Alembic`](https://alembic.sqlalchemy.org/) database migrate
  - WebUI(Required for appearance):
    - [`mistune`](https://mistune.lepture.com/) Markdown
    - [`Pygments`](https://https://pygments.org/) Let code colorful
  - WebUI(All):
    - Launch items
    - [`sanic_ext`](https://sanic.dev/en/plugins/sanic-ext/getting-started.html) Sanic's official extensions
  - Model:
    - [`torch`](https://pytorch.org)
    - [`safetensors`](https://github.com/huggingface/safetensors) A freamwork-agnostic method to load/store Tensors
  - Optional for security:
    - [`ecdsa`](https://github.com/tlsfuzzer/python-ecdsa) Cryptography
- Decoration for launch application
  - [**PicoCSS**](https://picocss.com)
- Front-end[Optional]
  - [**Node**](https://nodejs.org): If node installed, it will re-complie the front-end in `/webapp` folder. If you want to re-development, it is required
  - [**Tailwind CSS**](https://tailwindcss.com) for decorate
  - [**AppRun**](https://apprun.js.org) for SPA
  - [**Vite**](https://vitejs.dev/) as a frontend tooling

## Contributors

Myself, and...

## Thanks
