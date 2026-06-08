# 图片超分辨率工具

[![Latest Release](https://img.shields.io/github/v/release/qwertasdfg77/image-super-resolution-tool?label=latest)](https://github.com/qwertasdfg77/image-super-resolution-tool/releases/latest)
[![Download](https://img.shields.io/badge/download-single%20installer-brightgreen)](https://github.com/qwertasdfg77/image-super-resolution-tool/releases/latest)
[![Windows](https://img.shields.io/badge/Windows-10%20%2F%2011-0078d4)](https://github.com/qwertasdfg77/image-super-resolution-tool/releases/latest)
[![NVIDIA CUDA](https://img.shields.io/badge/NVIDIA-CUDA-76b900)](https://developer.nvidia.com/cuda-zone)
[![Models](https://img.shields.io/badge/models-ATD%20%7C%20HAT%20%7C%20Real--ESRGAN-orange)](THIRD_PARTY_NOTICES.md)
[![License](https://img.shields.io/github/license/qwertasdfg77/image-super-resolution-tool)](LICENSE)

Windows 图形界面图片超分工具。当前公开版本是 `v1.1.3`，面向普通用户使用，不需要写代码。

关键词：图片超分辨率、AI 放大、照片增强、动漫插画超分、NVIDIA CUDA、RTX 4060、ATD、HAT、Real-ESRGAN。

English version: [Image Super Resolution Tool](https://github.com/qwertasdfg77/image-super-resolution-tool-en)

## 下载

普通用户只需要到 Latest Release 下载一个文件：

- `ImageSuperResolutionTool-v1.1.3-Setup.exe`

Latest Release：
https://github.com/qwertasdfg77/image-super-resolution-tool/releases/latest

## 使用方式

1. 下载 `ImageSuperResolutionTool-v1.1.3-Setup.exe`。
2. 双击安装器。
3. 在弹出的窗口里选择安装位置。
4. 安装完成后，桌面会出现 `图片超分辨率工具` 快捷方式。
5. 第一次打开软件后，点击左下角 `安装/检查环境` 安装运行环境。

## 安装器包含什么

- 图形界面程序和超分脚本。
- ATD 官方超分辨率模型。
- HAT 高质量超分辨率模型。
- Real-ESRGAN 通用照片模型。
- Real-ESRGAN 动漫插画模型。
- 程序图标和桌面快捷方式创建逻辑。

安装器包含可直接打开软件界面的启动器。电脑没有预装 Python 时，也应先进入软件界面；第一次使用时点击软件内 `安装/检查环境`，程序会下载本地 Python 运行时、CUDA 版 PyTorch 和其它依赖。运行环境会安装到当前用户的本地数据目录，避免安装目录在桌面或受保护位置时写入失败。

## 主要功能

- 自动识别 NVIDIA 显卡型号、显存容量和当前空闲显存。
- 按显卡性能自动匹配更合适的处理占用。
- 默认使用 `ATD 官方超分辨率模型`。
- 内置四个模型，不需要用户单独下载模型。
- 自动调节锐化和去噪。
- 百分比进度条，显示已用时间和预计剩余时间。
- 支持单张图片和文件夹批量处理。
- 不保存上次输入图片路径和输出文件夹路径。
- 软件内不显示处理前后预览栏。

## 推荐配置

- Windows 10 / Windows 11
- NVIDIA RTX 4060 8GB 或更高
- 首次安装环境需要稳定网络和较大磁盘空间

## 说明

GitHub 源码仓库不直接存放大体积 `.pth` 模型文件；完整模型和安装器通过 Release 发布。

本工具不是游戏里的原生 DLSS。游戏里的原生 DLSS 需要游戏引擎提供多帧、运动向量和深度信息；本工具处理的是单张图片或图片文件夹。
