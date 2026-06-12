# 瑟菲洛桌宠 🖥️✨

Windows桌面右下角的AI小可爱——瑟菲洛住进你屏幕里啦！

## 功能

✅ 透明窗口，置顶显示
✅ 角色动画（支持GIF/逐帧）
✅ 双击弹出聊天窗口 → 调用DeepSeek AI对话
✅ 拖拽随意移动
✅ 右键菜单
✅ TTS语音回复（Edge TTS，晓伊音色）
✅ 默认占位图（没素材也能跑）

## 效果预览（占位模式）

```
┌──────────────┐
│    (◕‿◕)     │   ← 紫色小圆脸
│  双击聊天     │
│              │
│  💬 发送     │   ← 点击弹出聊天框
└──────────────┘
右下角，置顶
```

## 安装运行

### 1. 装Python（如果没装的话）

https://www.python.org/downloads/

装的时候**勾上"Add Python to PATH"** ✅

### 2. 装依赖

```cmd
pip install pillow requests edge-tts pywin32
```

> `pywin32` 是可选依赖，没有它也能跑，只是少了点击穿透功能

### 3. 配置API Key

打开 `config.py`，把这一行改成你的DeepSeek API Key：

```python
DEEPSEEK_API_KEY = "sk-你的key"
```

没有的话去 https://platform.deepseek.com 注册 → 创建一个API Key（免费送几百万token）

### 4. 开跑！

```cmd
python main.py
```

快捷键：`Esc` 退出

## 素材准备（后续）

往 `assets/animations/` 下放GIF文件，程序会自动加载：

```
assets/
├── animations/
│   ├── idle.gif         # 待机动画（循环）
│   ├── walk.gif         # 走路
│   ├── eat.gif          # 吃东西
│   └── wave.gif         # 打招呼
└── sounds/
    └── ...              # 音效（v0.2支持）
```

## 项目结构

```
sefiro-pet/
├── main.py            # 主程序
├── config.py          # 配置（API Key、窗口大小等）
├── requirements.txt   # 依赖列表
└── assets/
    ├── animations/    # GIF动画素材
    └── sounds/        # 音效
```

## 版本计划

| 版本 | 功能 |
|:----|:----|
| v0.1 🎉 | 透明窗口 + 动画 + 聊天 + TTS |
| v0.2 🔜 | 拖文件互动、多动作切换、设置面板 |
| v0.3 🔜 | 动作随机切换、小游戏、自定义皮肤 |
| v1.0 🚀 | 完整桌宠产品（可打包exe出售） |
