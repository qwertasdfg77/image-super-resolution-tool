# 常见问题

## 应该下载哪个文件？

普通用户优先下载 Release 页面里的 `ImageSuperResolutionToolWebSetup.exe`。它是小型联网安装器，会自动下载完整包、合并、校验、解压并创建快捷方式。

如果不想用安装器，也可以下载下面 4 个文件手动合并：

- `image-super-resolution-tool-full.zip.001`
- `image-super-resolution-tool-full.zip.002`
- `merge-full-package.ps1`
- `SHA256.txt`

## PowerShell 提示不能运行脚本怎么办？

在脚本所在文件夹里运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\install-from-github.ps1
```

如果是手动合并完整包，运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\merge-full-package.ps1
```

## CUDA 不可用怎么办？

先确认电脑有 NVIDIA 显卡，并更新 NVIDIA 显卡驱动。然后重新运行：

```text
install_gpu.bat
```

如果窗口里仍然显示 `CUDA: False`，通常是 PyTorch CUDA 版没有安装成功，或显卡驱动太旧。

## 第一次运行很慢正常吗？

正常。第一次可能会下载模型权重，完整包第一次启动也可能需要检查运行环境。后续会直接使用本地模型，速度会快很多。

## 显存不足怎么办？

建议先把“显卡占用”保持为“自动”。如果仍然显存不足，可以改成“保守”，或把放大倍数从 4 倍降到 2 倍/3 倍。

RTX 4060 8GB 建议使用“自动”。

## 输出图片太大怎么办？

放大倍数越高，输出尺寸和文件体积越大。建议使用 2 倍或 3 倍，或者输出后再用图片压缩工具压缩。

## 模型下载慢怎么办？

ATD Transformer 权重来自 Google Drive，网络慢时可能等待较久。可以稍后重试，或使用完整可运行包，因为完整包已经包含模型权重。

## 这个是不是游戏里的 DLSS？

不是。游戏里的 NVIDIA DLSS 需要游戏引擎提供多帧、运动向量和深度信息。本工具处理的是单张图片或图片文件夹，效果类似“AI 放大 + 清晰化”。

## 支持 AMD 或 Intel 显卡吗？

当前主要支持 NVIDIA CUDA。AMD/Intel GPU 暂不作为重点支持目标。

## 反馈问题需要提供什么？

建议提供：

- Windows 版本
- 显卡型号和显存
- 使用完整包、联网安装器还是源码版
- 软件窗口里的运行状态文字或截图
- 输入图片格式和尺寸
