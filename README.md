# 图片超分辨率工具

Windows 图形界面图片超分工具，支持 NVIDIA CUDA 显卡自动识别、显存自动匹配、ATD Transformer 超分模型、自动锐化和自动去噪。

## 适合谁

- 想把照片、截图、游戏画面、动漫图放大到 2 倍、3 倍或 4 倍的用户。
- 有 NVIDIA 显卡，推荐 RTX 4060 8GB 或更高。
- 想直接双击使用，不想写代码或手动调命令行参数的用户。

## 下载完整可运行版

打开 Release 页面：

[v1.0.0 完整包下载](https://github.com/qwertasdfg77/image-super-resolution-tool/releases/tag/v1.0.0)

下载这 4 个文件到同一个文件夹：

- `image-super-resolution-tool-full.zip.001`
- `image-super-resolution-tool-full.zip.002`
- `merge-full-package.ps1`
- `SHA256.txt`

在这个文件夹里打开 PowerShell，运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\merge-full-package.ps1
```

会生成 `image-super-resolution-tool-full.zip`。解压后双击：

```text
打开超分工具.bat
```

如果完整包里的运行环境在你的电脑上不可用，双击 `安装运行环境.bat` 重新安装一次即可。

## 使用源码版

源码仓库不包含 `.venv` 和模型权重。第一次使用请运行：

```text
安装运行环境.bat
```

安装完成后运行：

```text
打开超分工具.bat
```

第一次超分会自动下载模型权重到 `models` 文件夹。

## 功能

- 自动识别显卡型号、显存容量和当前空闲显存。
- 自动选择 tile、显存占用上限和推理精度。
- 默认使用 ATD x4 Transformer 模型。
- 支持 Real-ESRGAN 照片/动漫备用模型。
- 自动锐化和自动去噪。
- 百分比进度条，显示已用时间和预计剩余时间。
- 支持单张图片和整个文件夹批量处理。

## 说明

这个工具不是游戏里的原生 DLSS。原生 DLSS 需要游戏引擎提供多帧、运动向量和深度信息；本工具处理的是单张图片或图片文件夹。

更多细节见 [README_super_resolution.md](README_super_resolution.md)。
