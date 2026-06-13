#!/bin/bash
set -e

echo "========================================"
echo " 部署 ComfyUI"
echo "========================================"

cd ~

# 下载 ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Python 依赖
pip install -r requirements.txt

# 常用自定义节点
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
cd ..

# 创建模型目录
mkdir -p models/checkpoints models/loras models/vae models/controlnet

echo ""
echo "========================================"
echo " ✅ ComfyUI 部署完成"
echo "========================================"
echo ""
echo " 启动命令:"
echo "   cd ~/ComfyUI && python main.py --listen 0.0.0.0 --port 8188"
echo ""
echo " 访问: http://localhost:8188"
echo " 远程访问: http://$(hostname -I | awk '{print $1}'):8188"
echo ""
echo " 模型放这里:"
echo "   大模型: ~/ComfyUI/models/checkpoints/"
echo "   LoRA:   ~/ComfyUI/models/loras/"
echo "   VAE:    ~/ComfyUI/models/vae/"
echo "   ControlNet: ~/ComfyUI/models/controlnet/"
echo ""
