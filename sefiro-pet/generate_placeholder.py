#!/usr/bin/env python3
"""
生成瑟菲洛占位角色图（无GPU也能出可爱形象）
跑完后 assets/animations/ 下会生成 idle.gif
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets", "animations")
os.makedirs(ASSET_DIR, exist_ok=True)

# 调色板
SKIN = "#FDEBD0"
HAIR = "#8B4513"
HAIR_LIGHT = "#A0522D"
EYE_WHITE = "#FFFFFF"
EYE = "#2C3E50"
BLOUSH = "#FFB6C1"
MOUTH = "#E74C3C"
DRESS = "#9B59B6"
DRESS_DARK = "#8E44AD"

def draw_sefiro_frame(size, arm_offset=0, blink=False):
    """画一帧瑟菲洛"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    # --- 头发（后层） ---
    # 长发披肩
    hair_pts = [
        (cx-35, cy-35),  # 左上
        (cx-10, cy-50),   # 头顶左
        (cx+10, cy-50),   # 头顶右
        (cx+35, cy-35),   # 右上
        (cx+40, cy+10),   # 右耳
        (cx+45, cy+40),   # 右肩
        (cx+30, cy+55),   # 右下垂
        (cx+20, cy+45),   # 内收
        (cx-20, cy+45),   # 左下
        (cx-30, cy+55),   # 左传
        (cx-45, cy+40),   # 左肩
        (cx-40, cy+10),   # 左耳
    ]
    draw.polygon(hair_pts, fill=HAIR, outline=HAIR_LIGHT)

    # 刘海
    bangs = [
        (cx-30, cy-30),
        (cx-20, cy-38),
        (cx-5, cy-42),
        (cx+5, cy-42),
        (cx+20, cy-38),
        (cx+30, cy-30),
        (cx+25, cy-22),
        (cx+15, cy-28),
        (cx+5, cy-30),
        (cx-5, cy-30),
        (cx-15, cy-28),
        (cx-25, cy-22),
    ]
    draw.polygon(bangs, fill=HAIR_LIGHT)

    # 两侧长发
    draw.ellipse([cx-42, cy-25, cx-35, cy+35], fill=HAIR)
    draw.ellipse([cx+35, cy-25, cx+42, cy+35], fill=HAIR)

    # --- 脸 ---
    draw.ellipse([cx-30, cy-32, cx+30, cy+25], fill=SKIN, outline="#E8D5B7", width=1)

    # --- 眼睛 ---
    eye_spacing, eye_y = 14, cy-5
    for side in [-1, 1]:
        ex = cx + side * eye_spacing
        if blink:
            draw.arc([ex-8, eye_y+3, ex+8, eye_y+8], 0, 180, fill=EYE, width=3)
        else:
            draw.ellipse([ex-8, eye_y-5, ex+8, eye_y+5], fill=EYE_WHITE)
            draw.ellipse([ex-4, eye_y-3, ex+4, eye_y+3], fill=EYE)
            draw.ellipse([ex-1, eye_y-1, ex+2, eye_y+2], fill="white")  # 高光

    # --- 腮红 ---
    draw.ellipse([cx-22, cy+6, cx-12, cy+14], fill=BLOUSH, outline=None)
    draw.ellipse([cx+12, cy+6, cx+22, cy+14], fill=BLOUSH, outline=None)

    # --- 嘴巴 ---
    draw.arc([cx-8, cy+12, cx+8, cy+20], 0, 180, fill=MOUTH, width=2)

    # --- 身体 / 连衣裙 ---
    body_top = cy + 20
    body_pts = [
        (cx-30, body_top),      # 左肩
        (cx+30, body_top),      # 右肩
        (cx+35, body_top+40),   # 右下摆
        (cx-35, body_top+40),   # 左下摆
    ]
    draw.polygon(body_pts, fill=DRESS, outline=DRESS_DARK, width=1)

    # 领口装饰
    draw.polygon([
        (cx-8, body_top), (cx+8, body_top), (cx, body_top+12)
    ], fill="white")

    # --- 手臂（带摆动动画） ---
    arm_y = body_top + 5
    # 左臂
    draw.line([
        cx-30 + arm_offset, arm_y,
        cx-40 - arm_offset, arm_y + 25
    ], fill=SKIN, width=6, joint="curve")
    # 右臂
    draw.line([
        cx+30 - arm_offset, arm_y,
        cx+40 + arm_offset, arm_y + 25
    ], fill=SKIN, width=6, joint="curve")

    # --- 头顶蝴蝶结 ---
    bow_color = "#FF69B4"
    draw.ellipse([cx-12, cy-55, cx-2, cy-45], fill=bow_color)
    draw.ellipse([cx+2, cy-55, cx+12, cy-45], fill=bow_color)
    draw.ellipse([cx-5, cy-52, cx+5, cy-44], fill=bow_color)

    return img


def main():
    print("🎨 生成瑟菲洛占位角色图...")
    frames = []

    # 生成4帧，带不同的手臂摆动和眨眼
    for i in range(4):
        arm = 3 if i % 2 == 0 else -3
        blink = i == 3
        frame = draw_sefiro_frame(200, arm_offset=arm, blink=blink)
        frames.append(frame)

    # 保存为GIF
    out_path = os.path.join(ASSET_DIR, "idle.gif")
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=500,
        loop=0,
        transparency=0,
        disposal=2
    )
    print(f"✅ 已生成: {out_path}")
    print(f"   帧数: {len(frames)}，循环播放")

    # 也保存一帧静态图做预览
    preview = os.path.join(ASSET_DIR, "..", "preview.png")
    frames[0].save(preview)
    print(f"  预览图: {os.path.abspath(preview)}")


if __name__ == "__main__":
    main()
