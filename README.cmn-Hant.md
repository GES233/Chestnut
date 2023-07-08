# Chestnut 🌰

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black) [![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

[English](/README.md) [简体中文](/README.cmn-Hans.md)

Chestnut 是用於展示項目的基於 Web 的腳手架，使用了 Sanic 和 AppRun 構建，並從作者的某個私密倉庫（如果該項目成型也將會公開倉庫）克隆而來。

它的靈感來源於 [AUTOMATIC1111's WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 以及更早之前，通過編程方法完成並能夠隨機生成不同結果以供其他同學參考答案的作業。

特點：

- 領域驅動設計 + 整潔架構 => 便於拓展
- 更少的命令行參數
- 對門外漢（指不懂相關技術的人）友好

## TOC

- [第一步](#第一步)

## 第一步

配置好環境，下載程式碼並開啟引導應用。

```bash
Copy code
python virtualenv venv python=3.10
source venv/bin/activate
git clone https://github.com/GES233/Chestnut.git
python -m pip install -r requirements_basic.txt
python -m chestnut launch
```

當命令行出現相關訊息時，就說明引導應用成功運行。然後打開 http://127.0.0.1:6699 進行下一步操作。
