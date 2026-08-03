<div align="center">

# 💎 Aria Studio 

**面向带屏赛博智能键盘与多模态 AI 硬件的全能控制中心 & 驱动平台**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-green.svg)](https://flask.palletsprojects.com/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)

[简体中文](README.md) | [English](README_EN.md)

</div>

---

## 📖 项目简介 (Introduction)

**Aria Studio** 是一款专为超宽屏/双屏智能磁轴键盘及边缘计算设备（如 A527 主板）定制的上位机驱动与 AI 交互控制台。

项目结合了桌面端 PyQt/Tkinter 图形化控制台与嵌入式 Flask 边缘服务，支持 **跨设备 HTML 实时推送与渲染预览**、**系统硬件遥测**、**多模态 AI 模型交互（Gemini & DeepSeek）**、**超低延迟视频传输** 以及 **快捷按键与 URL 联动映射**。

---

## ✨ 核心特性 (Features)

* 🖥️ **DS Mini Viewport 持久化预览与渲染**：
  * 支持 1920x350 真实比例的 UI 实时快照渲染与本地持久化缓存。
  * 内置文本防卡死智能保护（对超长 Base64 编码与长文本数据自动折叠与截断）。
* 🤖 **双 Agent / 多 AI 引擎桥接**：
  * 内置 Gemini 1.5 Flash 与 DeepSeek V4 闪电模型 API 集中路由。
  * 支持语音上传 (`upload_voice`) 与实时 AI 文本回复/歌词同步显示。
* 📈 **赛博朋克极客遥测 (Telemetry HUD)**：
  * 50ms 阻尼高频 ECG 心电示波器与呼吸 LED 动态渲染 Canvas。
  * 实时抓取 PC 端的 CPU、RAM 占用及网络状态，并在终端硬件显示屏上高频同步。
* 🌐 **HTML 自由编写与无线推送**：
  * 内置多模板 HTML/CSS 编辑器，支持一键发送更新终端屏幕页面。
  * 智能剪贴板大代码拦截保护与自动备份机制。
* 🎬 **多媒体与智能快捷键联动**：
  * 视频/动态背景无线传输与覆盖功能。
  * 嵌入式全局按键与应用联动（如自动匹配打开 Google、YouTube、Discord 等页面）。

---

## 🏗️ 架构说明 (Architecture)

```text
┌─────────────────────────┐               HTTP / JSON (Port 8080)             ┌────────────────────────┐
│   Aria Studio 上位机    │  ───────────────────────────────────────────────► │   A527 硬件终端服务端  │
│   (client/app.py)       │  ◄─────────────────────────────────────────────── │   (server/a527_server.py)│
└───────────┬─────────────┘                                                   └───────────┬────────────┘
            │                                                                             │
            ├─► 渲染 1920x350 界面预览                                                      ├─► 部署嵌入式 HTML UI (index.html)
            ├─► 收集 CPU/RAM 遥测数据                                                        ├─► 路由 Gemini / DeepSeek API
            └─► 运行系统托盘 (pystray)                                                        └─► 托管视频资产与语音播放
