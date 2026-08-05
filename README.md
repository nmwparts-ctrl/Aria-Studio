<div align="center">

# 💎 Aria Studio

**All‑in‑One Control Center & Driver Platform for Cyber Smart Keyboards with Displays and Multimodal AI Hardware**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-green.svg)](https://flask.palletsprojects.com/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)

[简体中文](README.md) | [English](README_EN.md)

</div>

---

## 📖 Introduction

**Aria Studio** is a dedicated host driver and AI interaction console designed for ultra‑wide / dual‑screen smart magnetic‑switch keyboards and edge computing devices (such as the A527 board).

The project combines a desktop PyQt/Tkinter graphical console with an embedded Flask edge service, supporting **cross‑device HTML real‑time push and render preview**, **system hardware telemetry**, **multimodal AI model interaction (Gemini & DeepSeek)**, **ultra‑low latency video transmission**, and **shortcut key & URL mapping**.

---

## ✨ Key Features

* 🖥️ **DS Mini Viewport Persistent Preview & Rendering**
  * Real‑time snapshot rendering of UI at a true 1920×350 aspect ratio with local persistent caching.
  * Built‑in intelligent anti‑freeze protection (auto‑collapses and truncates oversized Base64 data and long text).

* 🤖 **Dual‑Agent / Multi‑AI Engine Bridge**
  * Centralised API routing for Gemini 1.5 Flash and DeepSeek V4 Lightning models.
  * Supports voice upload (`upload_voice`) and real‑time AI reply / lyrics sync display.

* 📈 **Cyberpunk Geek Telemetry (HUD)**
  * 50ms damped high‑frequency ECG oscilloscope with breathing LED dynamic rendering on Canvas.
  * Real‑time capture of PC CPU, RAM usage and network status, synchronised to the terminal display.

* 🌐 **HTML Free Editing & Wireless Push**
  * Built‑in multi‑template HTML/CSS editor with one‑click push to update the terminal screen.
  * Smart clipboard large‑code interception protection and auto‑backup mechanism.

* 🎬 **Multimedia & Smart Shortcut Linkage**
  * Wireless video/dynamic background transmission and overwrite.
  * Embedded global key‑to‑app mapping (e.g., automatically opens Google, YouTube, Discord, etc.).

* 📂 **Multi‑Functional HTML Page Library & Dynamic Switching**
  * Upload and save an unlimited number of custom HTML function files (e.g., game dashboards, system monitors, AI chat panels).
  * One‑click switch the current HTML app displayed on the hardware screen – hot‑reload in seconds without restarting the device.

---

## 🏗️ Architecture

```text
┌─────────────────────────┐               HTTP / JSON (Port 8080)             ┌────────────────────────┐
│   Aria Studio Host      │  ───────────────────────────────────────────────► │   Aria Hardware Server │
│   (client/app.py)       │  ◄─────────────────────────────────────────────── │ (server/Aria Bridge.py)│
└───────────┬─────────────┘                                                   └───────────┬────────────┘
            │                                                                             │
            ├─► Render 1920×350 interface preview                                        ├─► Deploy embedded HTML UI (index.html)
            ├─► Collect CPU/RAM telemetry data                                           ├─► Route Gemini / DeepSeek APIs
            └─► Run system tray (pystray)                                                └─► Host video assets and voice playback
