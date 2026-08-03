# 🧩 A527 多模态模板热更新引擎

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-0088CC?logo=tkinter&logoColor=white)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-0078D6?logo=windows&logoColor=white)](https://github.com)
[![AI Support](https://img.shields.io/badge/AI-Gemini%20%7C%20DeepSeek-4285F4?logo=google&logoColor=white)](https://deepseek.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?logo=github&logoColor=white)](https://github.com)

**A527 智能终端模板库** —— 专为 AI 算力服务器（如 NVIDIA HGX B300）打造的无重启式界面切换系统。  
你可以像更换手机壁纸一样，随时替换终端屏幕上的交互界面，且所有模板均支持调用后端 AI 能力（DeepSeek / Gemini）。

---

## 📸 核心价值

> **硬件算力固定，但交互界面无限。**  
> 无需烧录固件、无需重启服务，**1 秒切换模板**，让同一台 AI 服务器适应不同场景（运维监控、演示汇报、开发调试、客户体验）。

![演示效果](https://via.placeholder.com/800x400?text=Replace+with+your+Demo+GIF+or+Screenshot)

---

## 🏗️ 系统架构图

```mermaid
graph TD
    A[📦 templates/ 模板库] -->|Aria Studio 加载| B(🖥️ PC客户端)
    B -->|HTTP /update_html| C(🌉 Flask 后端桥接器)
    C -->|存储/托管| D[📂 a527_assets 缓存]
    C -->|API调用| E[☁️ Gemini / DeepSeek]
    C -->|返回遥测数据| B
    B -->|推送指令| C
    C -->|渲染| F[📟 A527 终端屏幕]
    F -->|用户交互| C
