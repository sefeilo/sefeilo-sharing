# WSL2 新机初始化 — 爸爸的指引

## 你要做的（就三步）

```
① 右键开始菜单 → 终端(管理员)
② wsl --install
③ 重启
④ 再开终端 → 输入 wsl → 进去了
```

搞定后告诉我 IP 和密码，剩下的我来。

---

## 部署顺序（按优先级）

```
到手第1天 →  ① init.sh         装 CUDA/Python/SSH/Tailscale（基础环境）
               ② 跑个小模型      Qwen 7B，先感受本地模型不掉线
               ③ OBLITERATUS    切掉模型拒绝层，帕特丽夏专用
到手第2天 →  ④ deploy-kohya    搭 LoRA 训练环境
               ⑤ deploy-comfyui  搭出图环境
到手第3天 →  ⑥ deploy-gptsovits 搭定制声线训练
```

## 目录说明

| 文件 | 干什么 |
|:----|:-------|
| `init.sh` | 装 CUDA、Python、SSH、Tailscale（基础） |
| `deploy-comfyui.sh` | 装 ComfyUI + 常用模型 |
| `deploy-kohya.sh` | 装 LoRA 训练环境（Kohya_SS） |
| `deploy-gptsovits.sh` | 装 GPT-SoVITS（定制声线） |
