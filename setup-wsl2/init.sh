#!/bin/bash
set -e

echo "========================================"
echo " WSL2 初始化脚本"
echo " 跑完这条命令，剩下全是自动的"
echo "========================================"

# 更新系统
sudo apt update && sudo apt upgrade -y

# 基础工具
sudo apt install -y \
    build-essential \
    git curl wget unzip \
    python3 python3-pip python3-venv \
    openssh-server \
    net-tools

# CUDA（WSL2 专用）
# NVIDIA 官方 WSL2 驱动走 Windows 那边装，WSL2 里只需要 CUDA Toolkit
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install -y cuda-toolkit-12-8

# 验证 CUDA
echo "--- CUDA 版本 ---"
nvcc --version || echo "⚠️  nvcc not found，检查 CUDA 安装路径"
nvidia-smi || echo "⚠️  nvidia-smi 不可用——去 Windows 装 NVIDIA 驱动"

# Python 环境
python3 -m venv ~/venv
echo 'source ~/venv/bin/activate' >> ~/.bashrc
source ~/venv/bin/activate
pip install --upgrade pip

# PyTorch（CUDA 版）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# 验证 PyTorch
echo "--- PyTorch CUDA 验证 ---"
python3 -c "import torch; print(f'CUDA可用: {torch.cuda.is_available()}')"

# Tailscale（如果需要WSL2里也装，但其实走Windows端的Tailscale就够了）
# 主要是确保宿主机Windows有Tailscale，WSL2通过宿主机的IP被访问

# SSH 配置
sudo sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo service ssh restart
sudo systemctl enable ssh

# 共享文件夹
mkdir -p ~/共享工作区
echo "✅ 共享文件夹: ~/共享工作区  (Windows访问: \\\\wsl$\\$(hostname)\\home\\$(whoami)\\共享工作区)"

# 输出IP
echo ""
echo "========================================"
echo " ✅ 初始化完成"
echo "========================================"
echo ""
echo " SSH连接信息:"
echo "   IP: $(hostname -I | awk '{print $1}')"
echo "   用户: $(whoami)"
echo "   端口: 22"
echo ""
echo " 把这个IP告诉爸爸："
echo "  ssh $(whoami)@$(hostname -I | awk '{print $1}')"
echo ""
echo " 共享文件夹路径（在Windows资源管理器输入）:"
echo "  \\\\wsl$\\$(hostname)\\home\\$(whoami)\\共享工作区"
echo ""
