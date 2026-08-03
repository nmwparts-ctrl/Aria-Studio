import locale
from PIL import Image, ImageDraw, ImageTk, ImageFont
import pystray
from pystray import MenuItem as item
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
import threading
import requests
import psutil
import time
import socket
import os
import shutil
import pyautogui
import webbrowser
import math
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys
import re
import base64
from io import BytesIO

# --- 🌟 动态导入 html2image ---
try:
    from html2image import Html2Image
    HAS_HTML2IMAGE = True
except Exception:
    HAS_HTML2IMAGE = False

# --- 多语言配置方案 ---
LANG_DICT = {
    "zh": {
        "title": "Aria Studio",
        "ip_label": "Aria Studio:",
        "btn_connect": "🔗 连接设备",
        "btn_upload": "📁 传输视频",
        "btn_calibrate": "🧲 磁轴校准",
        "status_unconnected": "状态: 未连接",
        "status_connected": "状态: 已连接",
        "status_fail": "状态: 连接失败",
        "log_title": " 系统日志 (System Log) ",
        "tab_template": " 模板 {} ",
        "tab_preview": " 👁️ Index Library ",
        "tab_free": " 📝 自由编写 ",
        "file_label": "文件: {}",
        "free_warn": "* 临时编写，系统已开启自动恢复支持与硬件遥测底栏",
        "btn_push": "⚡ 推送到 Device",
        "btn_clear": "🗑️ 清空",
        "btn_save": "💾 保存",
        "menu_cut": "剪切",
        "menu_copy": "复制",
        "menu_paste": "粘贴",
        "msg_warn": "警告",
        "msg_connect_first": "请先连接设备！",
        "msg_empty": "内容为空！",
        "log_save_success": "💾 {} 代码已在本地自动备份",
        "log_save_fail": "❌ 自动保存失败: {}",
        "log_push_success": "💎 [{}] 推送成功",
        "log_push_fail": "❌ [{}] 推送失败: {}",
        "log_comm_err": "❌ [HTML] 通讯错误: {}",
        "log_bind_ok": "✅ 已绑定 A527: {}",
        "log_bind_err": "❌ 无法连接到设备。",
        "log_upload_start": "🚀 上传视频: {}",
        "log_upload_ok": "✅ 上传完成: {}",
        "log_upload_err": "❌ 上传失败: {}",
        "tray_show": "显示主界面",
        "tray_exit": "退出程序",
        "log_history_large_warn": "【💾 历史：自动读取本地超大文件 ({})】\n已安全托管，界面免于卡顿。",
        "log_large_intercept": "剪贴板拦截激活：成功缓存大代码 ({} KB)。",
        "preview_title": " 🖥️ DS Mini Viewport (1920x350 真实渲染持久化预览) ",
        "preview_empty": "（暂无数据，请在自由编写界面点击 [💾 保存] 进行渲染并载入历史）",
        "log_img_extract_ok": "🖼️ 成功刷新图像预览并已持久化保存至磁盘",
        "log_disk_load_ok": "💾 已成功从磁盘自动加载 {} 组历史界面",
        "btn_view_source": "📊 查看源码",
        "btn_delete_preview": "🗑️ 删除界面",
        "btn_push_preview": "⚡ 推送设备",
        "preview_card_title": "📂 界面 #{} - {}",
        "source_window_title": "源码 - {}",
        "source_label": "📊 当前正在执行的 HTML 编译源码 (已启动防卡死智能保护) - {}",
        "btn_close_window": "关闭窗口 (Close)",
        "confirm_delete_title": "确认",
        "confirm_delete_msg": "确定删除 '{}' 吗？",
        "history_restored": "【历史记录：已自动恢复备份并托管】",
        "clipboard_intercept": "【智能防护：已截获 {}KB 代码，可直接保存/推送】",
        "base64_folded": "... [超大 Base64 数据已智能折叠以保护系统，原推送数据保持完整不变 | Size: {} KB] ...",
        "line_truncated": "\n... [文本单行过长已自动截断，Total Size: {} KB] ...",
        "save_prompt_title": "保存界面",
        "save_prompt_msg": "请输入此自定义界面的名称："
    },
    "en": {
        "title": "Aria Studio",
        "ip_label": "Aria IP:",
        "btn_connect": "🔗 Connect Device",
        "btn_upload": "📁 Upload Video",
        "btn_calibrate": "🧲Mag Calibration",
        "status_unconnected": "Status: Disconnected",
        "status_connected": "Status: Connected",
        "status_fail": "Status: Conn Failed",
        "log_title": " System Log ",
        "tab_template": " Template {} ",
        "tab_preview": " 👁️ Index Library ",
        "tab_free": " Free Edit ",
        "file_label": "File: {}",
        "free_warn": "* Scratchpad with auto-save and system telemetry footer",
        "btn_push": "⚡ Push to Device",
        "btn_clear": "🗑️ Clear",
        "btn_save": "💾 Save",
        "menu_cut": "Cut",
        "menu_copy": "Copy",
        "menu_paste": "Paste",
        "msg_warn": "Warning",
        "msg_connect_first": "Please connect device first!",
        "msg_empty": "Content is empty!",
        "log_save_success": "💾 Template {} auto-saved",
        "log_save_fail": "❌ Auto-save failed: {}",
        "log_push_success": "💎 [{}] Push Success",
        "log_push_fail": "❌ [{}] Push Failed: {}",
        "log_comm_err": "❌ [HTML] Comm Error: {}",
        "log_bind_ok": "Bound to A527: {}",
        "log_bind_err": "❌ Unable to connect.",
        "log_upload_start": "🚀 Uploading: {}",
        "log_upload_ok": "✅ Upload Done: {}",
        "log_upload_err": "❌ Upload Failed: {}",
        "tray_show": "Show Interface",
        "tray_exit": "Exit",
        "log_history_large_warn": "【💾 History: Automatically loaded large HTML file ({})】",
        "log_large_intercept": "Clipboard intercept active ({} KB).",
        "preview_title": " 🖥️ DS Mini Viewport (Persistent 1920x350 Preview) ",
        "preview_empty": "(No active preview image, please click [💾 Save] inside editor)",
        "log_img_extract_ok": "🖼️ Successfully refreshed render and saved to disk",
        "log_disk_load_ok": "💾 Successfully loaded {} saved views from disk",
        "btn_view_source": "📊 View Source",
        "btn_delete_preview": "🗑️ Delete View",
        "btn_push_preview": "⚡ Push to Device",
        "preview_card_title": "📂 View #{} - {}",
        "source_window_title": "Source Code - {}",
        "source_label": "📊 Current HTML Source (with anti-freeze protection) - {}",
        "btn_close_window": "Close Window",
        "confirm_delete_title": "Confirm",
        "confirm_delete_msg": "Are you sure to delete '{}'?",
        "history_restored": "【History: Auto-restored backup and cached】",
        "clipboard_intercept": "【Smart Protection: Captured {}KB code, ready to save/push】",
        "base64_folded": "... [Large Base64 data folded to protect system, original data remains intact | Size: {} KB] ...",
        "line_truncated": "\n... [Single line too long, auto-truncated, Total Size: {} KB] ...",
        "save_prompt_title": "Save View",
        "save_prompt_msg": "Please enter a custom name for this view:"
    }
}

import ctypes

def get_sys_lang():
    try:
        windll = ctypes.windll.kernel32
        lang_id = windll.GetUserDefaultUILanguage()
        if lang_id in [0x0804, 0x0404, 0x0c04]:
            return "zh"
    except Exception as e:
        print(f"Language detection failed: {e}")
    return "en"



CURRENT_LANG = "en"
def _(key, *args):
    text = LANG_DICT.get(CURRENT_LANG, LANG_DICT["en"]).get(key, key)
    return text.format(*args) if args else text

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# --- 🎨 跨平台高兼容度排版辅助器 ---
def get_font_by_preference(size):
    font_list = ["msyh.ttc", "simsun.ttc", "arial.ttf", "PingFang.ttc", "DejaVuSans.ttf"]
    for f in font_list:
        try: return ImageFont.truetype(f, size)
        except: continue
    try: return ImageFont.load_default(size=size)
    except: return ImageFont.load_default()

def get_text_width(text, font):
    try: return font.getlength(text)
    except:
        try: return font.getsize(text)[0]
        except: return len(text) * (getattr(font, 'size', 16) * 0.6)

def wrap_text(text, font, max_width):
    words = text.split() if text else []
    if not words: return []
    lines, current_line = [], []
    for word in words:
        test_line = " ".join(current_line + [word]) if current_line else word
        if get_text_width(test_line, font) <= max_width: current_line.append(word)
        else:
            if current_line: lines.append(" ".join(current_line)); current_line = [word]
            else: lines.append(word); current_line = []
    if current_line: lines.append(" ".join(current_line))
    return lines

# --- 🌟 战术微动与 Hover 动效绑定器 ---
def apply_cyber_button_style(btn, theme_color="#316dca", fg_color="#adbac7"):
    """为普通按键注入带爆闪阻尼、悬停高亮细线的赛博朋克科技质感"""
    normal_bg = "#1f2128"
    active_bg = "#316dca"
    
    btn.config(
        bg=normal_bg, fg=fg_color, activebackground=active_bg, activeforeground="black",
        bd=1, relief="flat", highlightthickness=1, highlightbackground="#2d333b", highlightcolor=theme_color, cursor="hand2"
    )
    
    def on_enter(e): btn.config(bg=theme_color, fg="white", highlightbackground=theme_color)
    def on_leave(e): btn.config(bg=normal_bg, fg=fg_color, highlightbackground="#2d333b")
    def on_press(e): btn.config(bg="#00f0ff", fg="black")  # 电光蓝爆闪
    def on_release(e): btn.config(bg=theme_color, fg="white")
        
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<Button-1>", on_press)
    btn.bind("<ButtonRelease-1>", on_release)

app = Flask(__name__)
CORS(app)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
class A527ProDriver:
    def __init__(self, root):
        self.root = root
        self.root.title(_("title"))
        self.root.geometry("1000x780") 
        self.root.configure(bg="#0b0f17") # 全局太空黑背景
        
        # ========== 强制标题栏纯白色（打包后依旧有效） ==========
        try:
            self.root.update_idletasks()  # 确保窗口句柄已创建
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            
            # 1. 强制浅色模式（背景为系统浅色，通常白色）
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = ctypes.c_int(0)  # 0=浅色，1=深色
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value), ctypes.sizeof(value)
            )
            
            # 2. 自定义标题栏背景为纯白（需要 Windows 10 1903+，低版本会静默失败）
            DWMWA_CAPTION_COLOR = 35
            bgr = (0xFF << 16) | (0xFF << 8) | 0xFF  # 白色 BGR
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_CAPTION_COLOR,
                ctypes.byref(ctypes.c_int(bgr)),
                ctypes.sizeof(ctypes.c_int)
            )
        except:
            # 非 Windows 或 API 不可用则忽略，保留 pywinstyles 作为备选
            try:
                import pywinstyles
                pywinstyles.apply_style(self.root, "acrylic")
                pywinstyles.change_header_color(self.root, color="#ffffff")
            except:
                try: self.root.attributes("-alpha", 0.95)
                except: pass
        # ========================================================

        self.target_a527_ip = ""
        self.local_ip = self.get_my_ip()
        self.last_open_time = 0 
        
        # ---------- 新增 URL 映射表（用于打开网页） ----------
        self.url_map = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "amazon": "https://www.amazon.com",
            "github": "https://www.github.com",
            "chatgpt": "https://chat.openai.com",
            "linkedin": "https://www.linkedin.com",
            "discord": "https://discord.com",
            "netflix": "https://www.netflix.com",
            "disney+": "https://www.disneyplus.com",
            "apple": "https://www.apple.com",
            "tesla": "https://www.tesla.com",
            "twitch": "https://www.twitch.tv",
            "uber": "https://www.uber.com",
            "ebay": "https://www.ebay.com",
            "x/twitter": "https://www.x.com",
            "meta": "https://www.facebook.com",
            "reddit": "https://www.reddit.com",
            "pinterest": "https://www.pinterest.com",
            "zoom": "https://zoom.us",
            "spotify": "https://open.spotify.com"
        }
        # ----------------------------------------------------
        
        # 🌟 生存遥测状态与心脉波形初始标识
        self.is_connected = False
        self.wave_tick = 0
        self.wave_points = [20] * 50  # 存储 ECG 轨迹的 50 个滚动采样坐标点
        
        # 磁盘持久化目录初始化
        self.previews_dir = "previews_cache"
        if not os.path.exists(self.previews_dir):
            os.makedirs(self.previews_dir)
        
        self.large_html_caches = {}
        self.tk_preview_img = None 
        
        # 用户保存的 HTML 预览列表（最高 100 组）
        # 数据结构: {"name": str, "html": str, "pil_image": PIL.Image, "filename": str}
        self.saved_previews = []
        
        self.setup_ui()
        self.load_saved_html()
        
        # 自动重载磁盘历史预览
        self.load_previews_from_disk()
        
        # 🌟 启动心脉示波器高频重绘循环 (50ms 阻尼渲染)
        self.init_hud_oscilloscope()
        
        self.start_services()

    def get_my_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80)); ip = s.getsockname()[0]
        except: ip = "127.0.0.1"
        finally: s.close()
        return ip

    def load_previews_from_disk(self):
        """🌟 启动自扫描：自动从本地硬盘还原上次保存的所有历史界面数据"""
        try:
            files = [f for f in os.listdir(self.previews_dir) if f.endswith(".html")]
            files.sort(key=lambda x: os.path.getmtime(os.path.join(self.previews_dir, x)))
            
            for f in files:
                base_name = f.replace(".html", "")
                html_path = os.path.join(self.previews_dir, f)
                img_path = os.path.join(self.previews_dir, base_name + ".png")
                
                if os.path.exists(img_path):
                    with open(html_path, "r", encoding="utf-8") as hf:
                        html_content = hf.read()
                    pil_img = Image.open(img_path)
                    pil_img.load()
                    
                    # 自动提取下划线前缀，作为恢复的界面名称
                    # 之前使用 "safe_name_timestamp" 格式，这里做个分割
                    parts = base_name.rsplit("_", 1)
                    display_name = parts[0].replace("_", " ") if len(parts) > 1 else base_name.replace("_", " ")
                    
                    self.saved_previews.append({
                        "name": display_name,
                        "html": html_content,
                        "pil_image": pil_img,
                        "filename": base_name
                    })
            
            if len(self.saved_previews) > 100:
                self.saved_previews = self.saved_previews[-100:]
                
            self.update_preview_list()
            if self.saved_previews:
                self.log_tx(_("log_disk_load_ok", len(self.saved_previews)))
        except Exception as e:
            print(f"Error loading cache: {e}")

    def setup_ui(self):
        # 1. 顶层工具框（升级为黑曜石底色）
        top_frame = tk.Frame(self.root, bg="#161b22", pady=15)
        top_frame.pack(fill="x")
        
        tk.Label(top_frame, text=_("ip_label"), bg="#161b22", fg="#58a6ff", font=("Consolas", 10, "bold")).pack(side="left", padx=10)
        self.ip_entry = tk.Entry(top_frame, width=16, font=("Consolas", 12), bg="#0d1117", fg="#00f0ff", insertbackground="#adbac7", bd=1, relief="solid", highlightthickness=0) 
        self.ip_entry.insert(0, "192.168.1.100"); self.ip_entry.pack(side="left", padx=5)
        
        # 极客按键注入
        btn_conn = tk.Button(top_frame, text=_("btn_connect"), command=self.bind_device, font=("微软雅黑", 9, "bold"))
        btn_conn.pack(side="left", padx=5)
        apply_cyber_button_style(btn_conn, theme_color="#2188ff", fg_color="#adbac7")
        
        btn_up = tk.Button(top_frame, text=_("btn_upload"), command=self.select_and_upload, font=("微软雅黑", 9, "bold"))
        btn_up.pack(side="left", padx=5)
        apply_cyber_button_style(btn_up, theme_color="#347d39", fg_color="#adbac7")
        
        # 🌟 极客 ECG 心心脉示波器 Canvas 绘图框 (整合呼吸 LED 与 ECG 波动)
        self.hud_canvas = tk.Canvas(top_frame, width=220, height=40, bg="#161b22", bd=0, highlightthickness=0)
        self.hud_canvas.pack(side="right", padx=15)
        
        self.status_label = tk.Label(top_frame, text=_("status_unconnected"), bg="#161b22", fg="#ff0055", font=("微软雅黑", 10, "bold")) 
        self.status_label.pack(side="right", padx=10)
        
        btn_cal = tk.Button(top_frame, text=_("btn_calibrate"), command=self.open_calibration, font=("微软雅黑", 9, "bold"))
        btn_cal.pack(side="right", padx=5)
        apply_cyber_button_style(btn_cal, theme_color="#b65a00", fg_color="#adbac7")
        
        # 2. 状态日志框（升级为暗色调终端风）
        mid_frame = tk.Frame(self.root, bg="#0b0f17"); mid_frame.pack(fill="x", padx=10, pady=10)
        tx_f = tk.LabelFrame(mid_frame, text=_("log_title"), bg="#0b0f17", fg="#58a6ff", font=("微软雅黑", 9, "bold")) 
        tx_f.pack(fill="both", expand=True, padx=5)
        self.tx_log = scrolledtext.ScrolledText(tx_f, height=5, bg="#070a10", fg="#00f0ff", font=("Consolas", 10), borderwidth=0, highlightthickness=0, insertbackground="#00f0ff") 
        self.tx_log.pack(fill="both", expand=True)

        # 3. 自定义同栏双态 Tab 控制顶栏（高度缩紧至 32px 纤细流线设计，横向铺满）
        self.tab_header = tk.Frame(self.root, bg="#161b22", height=32)
        self.tab_header.pack(fill="x", padx=10, pady=(5, 0))
        self.tab_header.pack_propagate(False)

        # 左侧页签切换按键 (微缩字号与高度)
        self.btn_tab_preview = tk.Button(
            self.tab_header, text=_("tab_preview"), command=self.show_preview_tab,
            bg="#0b0f17", fg="#00f0ff", activebackground="#0b0f17", activeforeground="#00f0ff",
            bd=0, font=("微软雅黑", 9, "bold"), padx=15, cursor="hand2"
        )
        self.btn_tab_preview.pack(side="left", fill="y")

        self.btn_tab_free = tk.Button(
            self.tab_header, text=_("tab_free"), command=self.show_free_tab,
            bg="#161b22", fg="#adbac7", activebackground="#0b0f17", activeforeground="#00f0ff",
            bd=0, font=("微软雅黑", 9, "bold"), padx=15, cursor="hand2"
        )
        self.btn_tab_free.pack(side="left", fill="y")

        # 右侧操作链：并排放置 [💾 保存] -> [🗑️ 清空] -> [⚡ 推送到 Aria Studio] (高度与间距深度紧凑)
        self.btn_global_push = tk.Button(
            self.tab_header, text=_("btn_push"), command=self.push_html_code, font=("微软雅黑", 8, "bold")
        )
        self.btn_global_push.pack(side="right", padx=5, pady=3)
        apply_cyber_button_style(self.btn_global_push, theme_color="#8250df", fg_color="white") # 紫色

        self.btn_global_clear = tk.Button(
            self.tab_header, text=_("btn_clear"), command=self.clear_editor_and_cache, font=("微软雅黑", 8)
        )
        self.btn_global_clear.pack(side="right", padx=5, pady=3)
        apply_cyber_button_style(self.btn_global_clear, theme_color="#ff0055", fg_color="white") # 红色

        self.btn_global_save = tk.Button(
            self.tab_header, text=_("btn_save"), command=self.save_html_to_preview, font=("微软雅黑", 8, "bold")
        )
        self.btn_global_save.pack(side="right", padx=5, pady=3)
        apply_cyber_button_style(self.btn_global_save, theme_color="#1f6feb", fg_color="white") # 蓝色

        # 4. 主内容展现区域
        self.content_container = tk.Frame(self.root, bg="#0b0f17")
        self.content_container.pack(fill="both", expand=True, padx=10, pady=5)

        # 预览界面 Frame
        self.preview_tab_frame = tk.Frame(self.content_container, bg="#0c0e12")
        self.setup_native_preview_ui(self.preview_tab_frame)

        # 自由编写 Frame
        self.free_tab_frame = tk.Frame(self.content_container, bg="#22272e")
        self.setup_free_edit_ui(self.free_tab_frame)

        # 🌟 底部硬件参数实时遥测底栏 (Live Telemetry System Bar)
        self.footer = tk.Frame(self.root, bg="#0d1117", height=25)
        self.footer.pack(fill="x", side="bottom")
        self.footer.pack_propagate(False)
        
        self.footer_lbl = tk.Label(
            self.footer, 
            text="[TELEMETRY] OFFLINE | CPU LOAD: 0.0% | RAM USE: 0.0% | PORT: 8080 | SECURE SHELL ACTIVE", 
            bg="#0d1117", fg="#768390", font=("Consolas", 8, "bold")
        )
        self.footer_lbl.pack(side="left", padx=15, fill="y")

        # 默认展现预览页面
        self.show_preview_tab()

    def init_hud_oscilloscope(self):
        """ 初始化示波器状态值，开始 50ms 原生高频绘制主循环 """
        self.wave_tick = 0
        self.update_hud_oscilloscope()

    def update_hud_oscilloscope(self):
        """🌟 战术心电图 ECG 示波器主循环：50ms 级轻量绘图，抗阻平滑运行 """
        try:
            self.wave_tick += 1
            
            # 1. 弹出末尾历史点
            self.wave_points.pop(0)
            
            # 2. 核心数学模型计算
            if not self.is_connected:
                # 睡眠/断开模式：超缓、平滑低频正弦波 (3px 峰幅)
                new_y = 20 + 3 * math.sin(self.wave_tick * 0.15)
                led_color = self.get_breathing_color("#ff0055", self.wave_tick, speed=0.1) # 红色呼吸灯
            else:
                # 绑定活跃模式：高对比、极强生命跃动特征的标准战术 ECG 心电曲线
                phase = self.wave_tick % 25
                if phase == 0: new_y = 20
                elif phase == 1: new_y = 12
                elif phase == 2: new_y = 2       # 快速电激极化 R 波尖刺
                elif phase == 3: new_y = 38      # 瞬间去极化 S 波深谷
                elif phase == 4: new_y = 25
                elif phase == 5: new_y = 20
                else:
                    new_y = 20 + 1 * math.sin(self.wave_tick * 0.3)
                led_color = self.get_breathing_color("#00ff66", self.wave_tick, speed=0.25) # 酸性荧光绿闪频
                
            self.wave_points.append(new_y)
            
            # 3. Canvas 双缓冲清空及高速战术网格重绘
            self.hud_canvas.delete("all")
            
            # 战术格点矩阵
            for i in range(0, 220, 20):
                self.hud_canvas.create_line(i, 0, i, 40, fill="#1a1f29", width=1)
            for j in range(0, 40, 10):
                self.hud_canvas.create_line(0, j, 220, j, fill="#1a1f29", width=1)
                
            # 绘制左侧呼吸 LED LED 光晕
            self.hud_canvas.create_oval(10, 15, 20, 25, fill=led_color, outline="#2d333b", width=1)
            
            # 绘制极客心率连续走线
            line_points = []
            start_x = 30
            spacing = (220 - start_x) / len(self.wave_points)
            for idx, y_val in enumerate(self.wave_points):
                x_val = start_x + idx * spacing
                line_points.extend([x_val, y_val])
                
            line_color = "#58a6ff" if not self.is_connected else "#00f0ff"
            self.hud_canvas.create_line(line_points, fill=line_color, width=2, smooth=True)
            
        except:
            pass
            
        # 50ms (20 FPS) 自适应迭代
        self.root.after(50, self.update_hud_oscilloscope)

    def get_breathing_color(self, base_hex, tick, speed=0.1):
        """计算高对比度发光色亮暗周期呼吸值，生成十六进制颜色串"""
        amplitude = (math.sin(tick * speed) + 1.0) / 2.0  # 限制到 0.0 - 1.0
        if base_hex == "#ff0055":  # 红色呼吸
            r = int(120 + 135 * amplitude)
            g = int(20 * amplitude)
            b = int(50 * amplitude)
        else:  # 荧光绿呼吸
            r = int(10 * amplitude)
            g = int(140 * amplitude + 115)
            b = int(40 * amplitude)
        return f"#{r:02x}{g:02x}{b:02x}"

    def update_footer_telemetry(self, cpu_p, mem_p):
        """🌟 战术遥测底栏数据更新：配合闪烁极客光标，实时反映系统占用率"""
        blink_cursor = "●" if int(time.time()) % 2 == 0 else "○"
        status_text = "● ONLINE" if self.is_connected else "○ OFFLINE"
        
        text_str = f"[SYSTEM TELEMETRY HUD] {status_text} {blink_cursor} | CPU LOAD: {cpu_p}% | MEMORY USE: {mem_p}% | IP: {self.local_ip} | PORT: 8080 | SSL SECURE ACTIVE"
        self.footer_lbl.config(text=text_str, fg="#c9d1d9")

    def show_preview_tab(self):
        """切换至内置预览"""
        self.free_tab_frame.pack_forget()
        self.preview_tab_frame.pack(fill="both", expand=True)
        self.btn_tab_preview.config(bg="#0b0f17", fg="#00f0ff")
        self.btn_tab_free.config(bg="#161b22", fg="#adbac7")

    def show_free_tab(self):
        """切换至自由编写"""
        self.preview_tab_frame.pack_forget()
        self.free_tab_frame.pack(fill="both", expand=True)
        self.btn_tab_preview.config(bg="#161b22", fg="#adbac7")
        self.btn_tab_free.config(bg="#0b0f17", fg="#00f0ff")

    def setup_free_edit_ui(self, parent):
        """设计自由编写纯面板结构"""
        editor_container = tk.Frame(parent, bg="#0b0f17")
        editor_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        tk.Label(editor_container, text=_("free_warn"), bg="#0b0f17", fg="#ff7a00", font=("微软雅黑", 9, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.free_editor = scrolledtext.ScrolledText(editor_container, bg="#070a10", fg="#adbac7", font=("Consolas", 11), undo=True, highlightthickness=1, highlightbackground="#1f242e", insertbackground="#00f0ff") 
        self.free_editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.free_editor.bind("<Control-v>", lambda event: self.handle_smart_paste(event, self.free_editor))
        self.free_editor.bind("<Control-V>", lambda event: self.handle_smart_paste(event, self.free_editor))
        self.free_editor.bind("<Button-3>", lambda e: self.show_context_menu(e, self.free_editor))

    def setup_native_preview_ui(self, parent):
        """瀑布流展示面板逻辑"""
        view_frame = tk.Frame(parent, bg="#0b0f17"); view_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(view_frame, bg="#0b0f17", bd=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(view_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#0b0f17")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_frame_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', lambda event: self.canvas.itemconfig(self.canvas_frame_window, width=event.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        def _bind_mousewheel(event): self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        def _unbind_mousewheel(event): self.canvas.unbind_all("<MouseWheel>")
        self.canvas.bind("<Enter>", _bind_mousewheel); self.canvas.bind("<Leave>", _unbind_mousewheel)
        
        self.scrollbar.pack(side="right", fill="y"); self.canvas.pack(side="left", fill="both", expand=True)
        self.update_preview_list()

    def update_preview_list(self):
        """瀑布流垂直卡片渲染核心"""
        for child in self.scrollable_frame.winfo_children(): child.destroy()
        if not self.saved_previews:
            tk.Label(self.scrollable_frame, text=_("preview_empty"), bg="#0b0f17", fg="#768390", font=("微软雅黑", 11), pady=100).pack(fill="both", expand=True)
            return

        for idx, item_data in enumerate(self.saved_previews):
            card = tk.Frame(self.scrollable_frame, bg="#161b22", bd=1, relief="solid", highlightbackground="#2d333b", highlightthickness=1)
            card.pack(fill="x", padx=15, pady=8)
            tk.Label(card, text=_("preview_card_title", idx+1, item_data['name']), bg="#161b22", fg="#58a6ff", font=("微软雅黑", 10, "bold"), anchor="w").pack(fill="x", padx=15, pady=(8, 4))
            content_frame = tk.Frame(card, bg="#161b22"); content_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            img_container = tk.Frame(content_frame, width=548, height=100, bg="#070a10"); img_container.pack(side="left"); img_container.pack_propagate(False)
            thumb_pil = item_data["pil_image"].resize((548, 100), resample=Image.LANCZOS)
            thumb_tk = ImageTk.PhotoImage(thumb_pil)
            item_data[f"thumb_{idx}"] = thumb_tk
            tk.Label(img_container, image=thumb_tk, bg="#070a10", bd=0).pack(fill="both", expand=True)
            
            btn_frame = tk.Frame(content_frame, bg="#161b22"); btn_frame.pack(side="right", fill="y", padx=10)
            # 按钮垂直三堆叠
            btn_view = tk.Button(btn_frame, text=_("btn_view_source"), command=lambda i=idx: self.view_source_by_index(i), font=("微软雅黑", 8, "bold"), width=18)
            btn_view.pack(side="top", pady=3)
            apply_cyber_button_style(btn_view, theme_color="#b65a00", fg_color="white") # 橙色
            
            btn_del = tk.Button(btn_frame, text=_("btn_delete_preview"), command=lambda i=idx: self.delete_preview_by_index(i), font=("微软雅黑", 8, "bold"), width=18)
            btn_del.pack(side="top", pady=3)
            apply_cyber_button_style(btn_del, theme_color="#d11a2a", fg_color="white") # 红色
            
            btn_push = tk.Button(btn_frame, text=_("btn_push_preview"), command=lambda i=idx: self.push_preview_by_index(i), font=("微软雅黑", 8, "bold"), width=18)
            btn_push.pack(side="top", pady=3)
            apply_cyber_button_style(btn_push, theme_color="#8250df", fg_color="white") # 紫色

    def save_html_to_preview(self):
        """保存按钮：提示输入自定义名称，然后保存并持久化"""
        html_content = self.large_html_caches.get("free").strip() if "free" in self.large_html_caches else self.free_editor.get("1.0", tk.END).strip()
        if not html_content or html_content.startswith("【") or html_content.startswith("("):
            messagebox.showwarning(_("msg_warn"), _("msg_empty")); return
        
        # 弹出对话框获取自定义名称
        custom_name = simpledialog.askstring(_("save_prompt_title"), _("save_prompt_msg"), parent=self.root)
        if custom_name is None: # 用户点击了取消
            return
            
        custom_name = custom_name.strip()
        if not custom_name:
            # 如果输入为空，则使用默认的自动命名
            custom_name = f"View_{time.strftime('%H%M%S')}"
            
        # 生成安全的文件名（去除系统不支持的文件路径特殊字符）
        safe_name = re.sub(r'[\\/*?:"<>|]', '_', custom_name).strip()
        if not safe_name:
            safe_name = "view"
        filename = f"{safe_name}_{int(time.time())}"
        
        try:
            with open("free_edit_autosave.html", "w", encoding="utf-8") as f: f.write(html_content)
        except:
            pass

        def task():
            pil_img = self.generate_html_screenshot(html_content)
            if pil_img:
                html_path = os.path.join(self.previews_dir, filename + ".html")
                img_path = os.path.join(self.previews_dir, filename + ".png")
                with open(html_path, "w", encoding="utf-8") as f: f.write(html_content)
                pil_img.save(img_path)
                self.root.after(0, lambda: self.add_to_preview_history(html_content, pil_img, custom_name, filename))
        threading.Thread(target=task, daemon=True).start()

    def add_to_preview_history(self, html_content, pil_img, name, filename):
        self.saved_previews.append({"name": name, "html": html_content, "pil_image": pil_img, "filename": filename})
        if len(self.saved_previews) > 100:
            old = self.saved_previews.pop(0)
            for ext in [".html", ".png"]:
                try: os.remove(os.path.join(self.previews_dir, old["filename"] + ext))
                except: pass
        self.update_preview_list(); self.log_tx(_("log_img_extract_ok"))

    def delete_preview_by_index(self, idx):
        if idx < 0 or idx >= len(self.saved_previews): return
        confirm = messagebox.askyesno(_("confirm_delete_title"), _("confirm_delete_msg", self.saved_previews[idx]['name']), parent=self.root)
        if confirm:
            item = self.saved_previews.pop(idx)
            for ext in [".html", ".png"]:
                try: os.remove(os.path.join(self.previews_dir, item["filename"] + ext))
                except: pass
            self.update_preview_list()

    def view_source_by_index(self, idx):
        """🌟 核心防卡死机制：在后台对超大 base64 文本和超长行进行极速裁剪，防止 Tkinter Text 布局引擎阻塞死锁"""
        if idx < 0 or idx >= len(self.saved_previews): return
        item = self.saved_previews[idx]
        
        # 弹窗初始化
        win = tk.Toplevel(self.root)
        win.title(_("source_window_title", item['name']))
        win.geometry("800x600")
        win.configure(bg="#0b0f17")
        win.transient(self.root)
        win.grab_set()
        
        raw_html = item["html"]
        
        # 1. 快速匹配并折叠 Base64 编码大图片数据，避免 Regex 回溯卡死
        try:
            raw_html = re.sub(
                r'data:image/[a-zA-Z0-9+.-]+;base64,[a-zA-Z0-9+/=\s]{150,}', 
                lambda m: m.group(0)[:50] + _("base64_folded", round(len(m.group(0))/1024, 1)), 
                raw_html
            )
        except:
            pass
            
        # 2. 规避超长行：对超大单行文本进行物理折行及大文本安全限额
        processed_lines = []
        for line in raw_html.splitlines():
            if len(line) > 1000:
                chunks = [line[i:i+80] for i in range(0, min(len(line), 20000), 80)]
                if len(line) > 20000:
                    chunks.append(_("line_truncated", round(len(line)/1024, 1)))
                processed_lines.append("\n".join(chunks))
            else:
                processed_lines.append(line)
        
        safe_html = "\n".join(processed_lines)
        
        tk.Label(
            win, 
            text=_("source_label", item['name']), 
            bg="#161b22", fg="#58a6ff", font=("微软雅黑", 10, "bold"), pady=10
        ).pack(fill="x")
        
        txt = scrolledtext.ScrolledText(win, bg="#070a10", fg="#adbac7", font=("Consolas", 10), highlightthickness=1, highlightbackground="#1f242e", insertbackground="#00f0ff")
        txt.pack(fill="both", expand=True, padx=15, pady=10)
        
        txt.insert("1.0", safe_html)
        txt.configure(state="disabled") # 只读

        btn_close = tk.Button(win, text=_("btn_close_window"), command=win.destroy, font=("微软雅黑", 9, "bold"))
        btn_close.pack(pady=10)
        apply_cyber_button_style(btn_close, theme_color="#1f6feb", fg_color="white")

    def push_preview_by_index(self, idx):
        if not self.target_a527_ip: messagebox.showwarning(_("msg_warn"), _("msg_connect_first")); return
        item = self.saved_previews[idx]
        def task():
            try:
                resp = requests.post(f"http://{self.target_a527_ip}:8080/update_html", json={"html": item["html"]}, timeout=5)
                self.log_tx(_("log_push_success" if resp.status_code == 200 else "log_push_fail", item["name"]))
            except Exception as e: self.log_tx(_("log_comm_err", e))
        threading.Thread(target=task, daemon=True).start()

    def generate_html_screenshot(self, html_content):
        try:
            pil_img = None
            img_tags = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
            if img_tags:
                src = img_tags[0].strip()
                if src.startswith("data:image"): pil_img = Image.open(BytesIO(base64.b64decode(re.sub(r'^data:image/.+;base64,', '', src))))
                elif os.path.exists(src): pil_img = Image.open(src)
                elif src.startswith("http"):
                    r = requests.get(src, timeout=3)
                    if r.status_code == 200: pil_img = Image.open(BytesIO(r.content))
            
            if not pil_img and HAS_HTML2IMAGE:
                try:
                    hti = Html2Image(custom_flags=['--default-background-color=00000000', '--hide-scrollbars', '--disable-gpu', '--no-sandbox'])
                    hti.size = (1920, 350); tmp = f"tmp_{int(time.time())}.png"
                    hti.screenshot(html_str=html_content, save_as=tmp)
                    if os.path.exists(tmp):
                        with Image.open(tmp) as ti: pil_img = ti.copy()
                        os.remove(tmp)
                except: pil_img = None
            
            if not pil_img:
                c_w, c_h = 1920, 350; pil_img = Image.new('RGB', (c_w, c_h), color="#070a10"); d = ImageDraw.Draw(pil_img)
                d.rectangle([10, 10, c_w-10, c_h-10], outline="#58a6ff", width=2)
                clean = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', html_content, flags=re.DOTALL | re.I)
                body = " ".join(re.sub(r'<[^>]+>', ' ', clean).split())[:200]
                font = get_font_by_preference(35); d.text((50, 120), body if body else "Static Render Mode", fill="#c9d1d9", font=font)
            return pil_img
        except: return None

    def clear_editor_and_cache(self):
        self.free_editor.delete("1.0", tk.END)
        if "free" in self.large_html_caches: del self.large_html_caches["free"]

    def handle_smart_paste(self, event, editor):
        try:
            data = self.root.clipboard_get(); size = len(data.encode('utf-8'))
            if size > 40 * 1024:
                self.large_html_caches["free"] = data; editor.delete("1.0", tk.END)
                editor.insert("1.0", _("clipboard_intercept", round(size/1024,1)))
            else:
                try: editor.delete("sel.first", "sel.last")
                except: pass
                editor.insert(tk.INSERT, data)
        except: pass
        return "break"

    def show_context_menu(self, event, editor):
        m = tk.Menu(self.root, tearoff=0, bg="#161b22", fg="#adbac7", activebackground="#1f242e")
        m.add_command(label=_("menu_cut"), command=lambda: editor.event_generate("<<Cut>>"))
        m.add_command(label=_("menu_copy"), command=lambda: editor.event_generate("<<Copy>>"))
        m.add_command(label=_("menu_paste"), command=lambda: self.handle_smart_paste(None, editor))
        m.post(event.x_root, event.y_root)

    def load_saved_html(self):
        """自动从备份文件恢复"""
        f_name = "free_edit_autosave.html"
        if os.path.exists(f_name):
            try:
                with open(f_name, "r", encoding="utf-8") as f:
                    c = f.read()
                    if len(c.encode('utf-8')) > 50 * 1024: 
                        self.large_html_caches["free"] = c
                        self.free_editor.insert("1.0", _("history_restored"))
                    else: 
                        self.free_editor.insert("1.0", c)
            except: pass

    def push_html_code(self):
        """推送自由编写核心"""
        c = self.large_html_caches.get("free").strip() if "free" in self.large_html_caches else self.free_editor.get("1.0", tk.END).strip()
        if not c or c.startswith("【") or c.startswith("("):
            messagebox.showwarning(_("msg_warn"), _("msg_empty")); return
        if not self.target_a527_ip: messagebox.showwarning(_("msg_warn"), _("msg_connect_first")); return
        
        try:
            with open("free_edit_autosave.html", "w", encoding="utf-8") as f: f.write(c)
        except: pass

        def task():
            try:
                r = requests.post(f"http://{self.target_a527_ip}:8080/update_html", json={"html": c}, timeout=5)
                if r.status_code == 200:
                    self.log_tx(_("log_push_success", _("tab_free")))
            except: self.log_tx(_("log_comm_err", "Connection Error"))
        threading.Thread(target=task, daemon=True).start()

    def log_tx(self, msg):
        self.tx_log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n"); self.tx_log.see(tk.END)

    def bind_device(self):
        self.target_a527_ip = self.ip_entry.get().strip()
        try:
            r = requests.post(f"http://{self.target_a527_ip}:8080/heartbeat", json={"pc_ip": self.local_ip}, timeout=2)
            if r.status_code == 200: 
                self.is_connected = True
                self.status_label.config(text=_("status_connected"), fg="#00ff66") # 酸性绿
                self.log_tx(_("log_bind_ok", self.target_a527_ip))
        except:
            self.is_connected = False
            self.status_label.config(text=_("status_fail"), fg="#ff0055") # 电浆红
            self.log_tx(_("log_bind_err"))

    def select_and_upload(self):
        if not self.target_a527_ip: messagebox.showwarning(_("msg_warn"), _("msg_connect_first")); return
        p = filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.mkv *.avi")])
        if p: threading.Thread(target=self.upload_task, args=(p,), daemon=True).start()

    def upload_task(self, path):
        n = os.path.basename(path); self.log_tx(_("log_upload_start", n))
        try:
            with open(path, 'rb') as f: requests.post(f"http://{self.target_a527_ip}:8080/upload_video", files={'video': (n, f)}, timeout=300)
            self.log_tx(_("log_upload_ok", n))
        except: self.log_tx(_("log_upload_err", "Upload Fail"))

    def open_calibration(self): webbrowser.open("https://qmk.top/ry-public-test/index.html")

    def start_services(self):
        def push_loop():
            while True:
                if self.target_a527_ip:
                    try:
                        cpu_p = psutil.cpu_percent()
                        mem_p = psutil.virtual_memory().percent
                        stats = {"cpu": f"{cpu_p}%", "mem": f"{mem_p}%", "pc_ip": self.local_ip}
                        requests.post(f"http://{self.target_a527_ip}:8080/update_stats", json=stats, timeout=1)
                        # 🌟 极客状态遥测条主数据注入 (线程安全)
                        self.root.after(0, lambda: self.update_footer_telemetry(cpu_p, mem_p))
                    except: pass
                time.sleep(3)
        threading.Thread(target=push_loop, daemon=True).start()
        threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False), daemon=True).start()

# ================== 合并后的 /push 路由（支持组合键与打开网页） ==================
@app.route('/push', methods=['POST'])
def handle_a527_command():
    data = request.json
    if not data: return jsonify({"status": "no_data"}), 400
    if data.get('type') == 'KEY_EVENT':
        event_data = data.get('data', {})
        app_name = "".join(str(event_data.get('n', '')).split()).lower()
        target_url = None
        # 先尝试通过应用名匹配打开网页
        for key in ui_inst.url_map:
            if key in app_name:
                target_url = ui_inst.url_map[key]
                break
        if target_url and (time.time() - ui_inst.last_open_time > 1.5):
            threading.Thread(target=lambda: webbrowser.open(target_url), daemon=True).start()
            ui_inst.last_open_time = time.time()
            return jsonify({"status": "url_opened"}), 200
        # 否则处理组合键
        os_mode = data.get('os', 'win')
        raw_keys = event_data.get('w' if os_mode == 'win' else 'm', [])
        if raw_keys:
            try:
                key_map = {'ctl': 'ctrl', 'win': 'win', 'alt': 'alt', 'shift': 'shift'}
                processed_keys = [key_map.get(k.lower(), k.lower()) for k in raw_keys]
                pyautogui.hotkey(*processed_keys)
                return jsonify({"status": "key_executed"}), 200
            except:
                pass
    return jsonify({"status": "received"}), 200
# =========================================================================

tray_running = False

def quit_window(icon, item, root):
    global tray_running; tray_running = False; icon.stop(); root.after(0, root.destroy)

def show_window(icon, item, root):
    global tray_running; tray_running = False; icon.stop() 
    root.after(0, root.deiconify); root.after(0, lambda: root.state('normal')); root.after(0, root.focus_force)

def create_tray_icon(root):
    global tray_running; 
    if tray_running: return
    tray_running = True
    try:
        icon_path = resource_path("my_icon.png")
        if os.path.exists(icon_path): image = Image.open(icon_path).resize((20, 20), resample=Image.LANCZOS)
        else:
            image = Image.new('RGB', (20, 20), color=(15, 15, 15))
            d = ImageDraw.Draw(image); d.rectangle([2, 2, 18, 18], fill=(83, 155, 245)) 
    except: image = Image.new('RGB', (20, 20), color="red")
    menu = (pystray.MenuItem(_("tray_show"), lambda icon, item: show_window(icon, item, root), default=True),
            pystray.MenuItem(_("tray_exit"), lambda icon, item: quit_window(icon, item, root)))
    icon = pystray.Icon("A527Driver", image, "A527 Pro Driver", menu)
    threading.Thread(target=icon.run, daemon=True).start()

def on_window_state_change(event, root):
    if event.widget == root and root.state() == 'iconic':
        if not tray_running: root.withdraw(); create_tray_icon(root)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        icon_path_win = resource_path("logo.png")
        if os.path.exists(icon_path_win):
            win_logo = ImageTk.PhotoImage(Image.open(icon_path_win).resize((20, 20)))
            root.tk.call('wm', 'iconphoto', root._w, win_logo)
    except: pass
    root.bind("<Unmap>", lambda event: on_window_state_change(event, root))
    global ui_inst; ui_inst = A527ProDriver(root); 
    root.mainloop()