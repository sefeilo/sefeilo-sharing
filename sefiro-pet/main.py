#!/usr/bin/env python3
"""
瑟菲洛桌宠 v0.1
Windows桌面宠物——透明窗口、角色动画、AI对话、语音
"""

import tkinter as tk
from tkinter import simpledialog, scrolledtext
import threading
import time
import json
import os
import sys
import asyncio
import requests
from io import BytesIO
from PIL import Image, ImageTk, ImageSequence

import config


# ============================================================
# TTS 引擎（使用 edge-tts，纯异步）
# ============================================================
def speak(text):
    """在子线程里跑 TTS，不阻塞主界面"""
    def _run():
        try:
            async def _speak():
                import edge_tts
                communicate = edge_tts.Communicate(
                    text[:500], config.TTS_VOICE,  # 截短避免超长
                    rate=config.TTS_SPEED
                )
                await communicate.save("__sefiro_tts__.mp3")
                os.startfile("__sefiro_tts__.mp3")  # Windows only
            asyncio.run(_speak())
        except ImportError:
            pass  # 没装 edge-tts，静默跳过
        except Exception as e:
            print(f"[TTS 提示] 语音没成功（不影响聊天）: {e}")
    threading.Thread(target=_run, daemon=True).start()


# ============================================================
# AI 对话
# ============================================================
def ai_chat(user_input):
    """调用 DeepSeek API，返回 AI 回复"""
    try:
        resp = requests.post(
            config.DEEPSEEK_API_URL,
            headers={
                "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": config.AI_MODEL,
                "messages": [
                    {"role": "system", "content": config.SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                "stream": False,
                "max_tokens": 500
            },
            timeout=30
        )
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"啊哦，脑子卡了：{e}"


# ============================================================
# 动画引擎（GIF 播放器）
# ============================================================
class GifPlayer:
    """加载并播放 GIF/静止图"""

    def __init__(self, canvas, x=10, y=10):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.frames = []
        self.durations = []
        self.total_frames = 0
        self.current_frame = 0
        self.image_item = None
        self.running = False
        self.after_id = None

    def load(self, filepath, size=(180, 180)):
        """加载 GIF 文件"""
        self.frames.clear()
        self.durations.clear()
        try:
            img = Image.open(filepath)
            for frame in ImageSequence.Iterator(img):
                frame = frame.convert("RGBA").resize(size, Image.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame))
                duration = frame.info.get("duration", 100)
                self.durations.append(duration if duration > 20 else 100)
            self.total_frames = len(self.frames)
            return True
        except Exception as e:
            print(f"[GIF Load Error] {e}")
            return False

    def load_placeholder(self, size=(180, 180)):
        """没有素材时显示占位图（渐变圆）"""
        from PIL import ImageDraw
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([5, 5, size[0]-5, size[1]-5], fill="#E0B0FF", outline="#DDA0DD", width=3)
        # 画眼睛
        eye_y = size[0] // 3
        draw.ellipse([55, eye_y-10, 75, eye_y+10], fill="white")
        draw.ellipse([105, eye_y-10, 125, eye_y+10], fill="white")
        draw.ellipse([62, eye_y-5, 68, eye_y+5], fill="#333")
        draw.ellipse([112, eye_y-5, 118, eye_y+5], fill="#333")
        # 画嘴巴
        draw.arc([65, eye_y+20, 115, eye_y+50], 0, 180, fill="#FF69B4", width=2)
        self.frames = [ImageTk.PhotoImage(img)]
        self.durations = [3000]
        self.total_frames = 1

    def start(self):
        """开始播放动画"""
        if self.total_frames == 0:
            return
        self.running = True
        self._play_frame()

    def _play_frame(self):
        if not self.running:
            return
        if self.image_item:
            self.canvas.delete(self.image_item)
        self.image_item = self.canvas.create_image(
            self.x, self.y, anchor="nw", image=self.frames[self.current_frame]
        )
        self.current_frame = (self.current_frame + 1) % self.total_frames
        self.after_id = self.canvas.after(
            self.durations[self.current_frame % len(self.durations)],
            self._play_frame
        )

    def stop(self):
        self.running = False
        if self.after_id:
            self.canvas.after_cancel(self.after_id)


# ============================================================
# 对话窗口（独立弹窗）
# ============================================================
class ChatWindow(tk.Toplevel):
    """独立的聊天对话框"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("💬 和瑟菲洛聊天")
        self.geometry("360x480")
        self.configure(bg="#1a1a2e")

        # 消息显示区
        self.msg_area = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, bg="#16213e", fg="#eee",
            font=("微软雅黑", 10), bd=0, padx=10, pady=10,
            state=tk.DISABLED
        )
        self.msg_area.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 4))

        # 输入框 + 发送按钮
        bottom_frame = tk.Frame(self, bg="#1a1a2e")
        bottom_frame.pack(fill=tk.X, padx=8, pady=(4, 8))

        self.input_entry = tk.Entry(
            bottom_frame, bg="#1a1a3e", fg="white",
            font=("微软雅黑", 10),
            insertbackground="white", relief=tk.SUNKEN, bd=2
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 4))
        self.input_entry.bind("<Return>", self.send_message)
        # 添加提示文字
        self.input_entry.insert(0, "点这里输入消息...")
        self.input_entry.bind("<FocusIn>", lambda e: self.input_entry.delete(0, tk.END) if self.input_entry.get() == "点这里输入消息..." else None)

        send_btn = tk.Button(
            bottom_frame, text="发送", bg="#e94560", fg="white",
            font=("微软雅黑", 9, "bold"), relief=tk.FLAT,
            padx=15, command=self.send_message
        )
        send_btn.pack(side=tk.RIGHT, padx=(8, 0))

        # 初始问候
        self.add_message("瑟菲洛", "嘿爸爸！找我聊天吗～😊")

    def add_message(self, sender, text):
        self.msg_area.config(state=tk.NORMAL)
        tag = "me" if sender == "你" else "sefiro"
        self.msg_area.insert(tk.END, f"{sender}: ", tag)
        self.msg_area.insert(tk.END, f"{text}\n\n")
        self.msg_area.config(state=tk.DISABLED)
        self.msg_area.see(tk.END)

    def send_message(self, event=None):
        text = self.input_entry.get().strip()
        if not text:
            return
        self.input_entry.delete(0, tk.END)
        self.add_message("你", text)

        # 在子线程中调用 AI
        def reply():
            response = ai_chat(text)
            self.after(0, lambda: self.add_message("瑟菲洛", response))
            # 非阻塞 TTS
            threading.Thread(target=lambda: speak(response), daemon=True).start()

        threading.Thread(target=reply, daemon=True).start()


# ============================================================
# 主窗口（透明桌宠）
# ============================================================
class PetWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("瑟菲洛")

        # --- 窗口配置 ---
        w, h = config.WINDOW_WIDTH, config.WINDOW_HEIGHT
        self.root.geometry(f"{w}x{h}+{self.root.winfo_screenwidth()-w-20}+{self.root.winfo_screenheight()-h-60}")
        self.root.overrideredirect(True)           # 无边框
        self.root.attributes("-topmost", True)      # 置顶
        self.root.attributes("-transparentcolor", config.TRANSPARENT_COLOR)
        self.root.configure(bg=config.TRANSPARENT_COLOR)

        # --- Canvas（画角色） ---
        self.canvas = tk.Canvas(
            self.root, width=w, height=h,
            bg=config.TRANSPARENT_COLOR,
            highlightthickness=0, bd=0
        )
        self.canvas.pack()
        self.canvas.configure(bg=config.TRANSPARENT_COLOR)

        # --- 拖拽功能 ---
        self.drag_data = {"x": 0, "y": 0, "dragging": False}
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_end)

        # --- 双击打开聊天 ---
        self.canvas.bind("<Double-Button-1>", self.open_chat)

        # --- 右键菜单 ---
        if hasattr(self, "_create_context_menu"):
            self.canvas.bind("<Button-3>", self._create_context_menu)

        # --- 动画 ---
        self.gif_player = GifPlayer(self.canvas, x=10, y=30)
        # 优先加载素材，没有就用占位图
        gif_path = os.path.join(config.ASSET_DIR, "animations", "idle.gif")
        if os.path.exists(gif_path):
            self.gif_player.load(gif_path)
        else:
            self.gif_player.load_placeholder()
        self.gif_player.start()

        # --- 状态标签（小字） ---
        self.status_label = self.canvas.create_text(
            100, 12, text="双击聊天", fill="#999",
            font=("微软雅黑", 8)
        )

        # --- 关闭快捷键 ---
        self.root.bind("<Escape>", lambda e: self.quit())

        # --- Windows 透明穿透（可选，需要 pywin32） ---
        self._enable_click_through(False)

    def _enable_click_through(self, enabled):
        """让鼠标穿透透明区域（只点击角色区域才有反应）"""
        try:
            import win32gui
            import win32con
            import win32api
            hwnd = win32gui.FindWindow(None, "瑟菲洛")
            if hwnd:
                ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                if enabled:
                    ex_style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
                else:
                    ex_style &= ~win32con.WS_EX_TRANSPARENT
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
        except ImportError:
            pass  # 没有 pywin32 也能用，只是不能穿透

    def on_drag_start(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["dragging"] = True

    def on_drag_move(self, event):
        if self.drag_data["dragging"]:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            x = self.root.winfo_x() + dx
            y = self.root.winfo_y() + dy
            self.root.geometry(f"+{int(x)}+{int(y)}")

    def on_drag_end(self, event):
        self.drag_data["dragging"] = False

    def open_chat(self, event=None):
        ChatWindow(self.root)

    def quit(self):
        self.gif_player.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


# ============================================================
# 入口
# ============================================================
def main():
    print("=" * 40)
    print("  瑟菲洛桌宠 v0.1")
    print("  Esc = 退出 | 双击 = 聊天 | 拖拽 = 移动")
    print("=" * 40)

    # 检查配置
    if not config.DEEPSEEK_API_KEY or "your-key" in config.DEEPSEEK_API_KEY:
        print("\n⚠️  请先在 config.py 里填你的 DeepSeek API Key")
        print("   没有的话去 https://platform.deepseek.com 注册\n")

    pet = PetWindow()

    # 加上右键菜单（需要窗口创建后才能绑定）
    def _menu(event):
        menu = tk.Menu(pet.root, tearoff=0, bg="#16213e", fg="#eee")
        menu.add_command(label="💬 聊天", command=pet.open_chat)
        menu.add_command(label="😴 休眠", command=lambda: None)
        menu.add_separator()
        menu.add_command(label="❌ 退出", command=pet.quit)
        menu.tk_popup(event.x_root, event.y_root)
    pet.canvas.bind("<Button-3>", _menu)

    pet.run()


if __name__ == "__main__":
    main()
