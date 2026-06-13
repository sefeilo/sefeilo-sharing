#!/bin/bash
set -e

echo "========================================"
echo " 部署 GPT-SoVITS（定制声线）"
echo "========================================"

cd ~

# 克隆 GPT-SoVITS
git clone https://github.com/RVC-Boss/GPT-SoVITS.git
cd GPT-SoVITS

# Python 环境
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

# 安装依赖（CPU + CUDA）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt

# 额外需要的
pip install ffmpeg-python soundfile librosa

echo ""
echo "========================================"
echo " ✅ GPT-SoVITS 部署完成"
echo "========================================"
echo ""
echo " 启动命令:"
echo "   cd ~/GPT-SoVITS && source venv/bin/activate && python webui.py"
echo ""
echo " 训练流程:"
echo "   ① 准备 3-10 分钟干净人声（WAV/MP3）"
echo "   ② 放 ~/共享工作区/voice-samples/"
echo "   ③ 开 WebUI → 语音切分 → 训练 → 推理"
echo ""
echo " 模型输出: ~/GPT-SoVITS/weights/"
echo ""
