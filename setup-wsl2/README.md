# WSL2 新机初始化 — 爸爸的指引

## 你要做的（就三步）

```
① 右键开始菜单 → 终端(管理员)
② wsl --install
③ 重启
④ 再开终端 → 输入 wsl → 进去了
```

搞定后告诉我，剩下的我来。

---

## 目录说明

| 文件 | 谁跑 | 干什么 |
|:----|:----|:-------|
| `init.sh` | 我 SSH 进去跑 | 装 CUDA、Python、Tailscale、SSH |
| `deploy-comfyui.sh` | 我跑 | 装 ComfyUI + 常用模型 |
| `deploy-kohya.sh` | 我跑 | 装 LoRA 训练环境 |
| `deploy-gptsovits.sh` | 我跑 | 装 GPT-SoVITS（定制声线） |
