#!/bin/bash
set -e

echo "========================================"
echo " 部署 Kohya_SS (LoRA 训练环境)"
echo "========================================"

cd ~

# 克隆 Kohya_SS
git clone https://github.com/bmaltais/kohya_ss.git
cd kohya_ss

# 安装
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Kohya 依赖
pip install -r requirements.txt

# 安装 bitsandbytes（WSL2 CUDA）
pip install bitsandbytes

# xformers（加速）
pip install xformers --index-url https://download.pytorch.org/whl/cu128

echo ""
echo "========================================"
echo " ✅ Kohya_SS 部署完成"
echo "========================================"
echo ""
echo " 启动命令:"
echo "   cd ~/kohya_ss && source venv/bin/activate && python kohya_gui.py --listen 0.0.0.0 --port 7860 --headless"
echo ""
echo " 访问: http://localhost:7860"
echo " 远程访问: http://$(hostname -I | awk '{print $1}'):7860"
echo ""
echo " 训练数据建议放在: ~/共享工作区/lora-training/"
echo " 模型输出: ~/共享工作区/lora-output/"
echo ""
