# 图片超分辨率工具

Windows 图形界面图片超分工具。当前公开版本是 `v1.0.3` 轻量版，面向普通用户使用，不需要写代码。

## 下载

请到 Latest Release 下载：

- `ImageSuperResolutionTool-Lightweight.zip`：推荐，下载后解压使用。
- `下载轻量版.bat`：可选，会自动下载并解压轻量包。
- `SHA256.txt`：用于校验下载文件。

Release 页面：
https://github.com/qwertasdfg77/image-super-resolution-tool/releases/latest

## 使用方法

1. 解压 `ImageSuperResolutionTool-Lightweight.zip`。
2. 双击 `打开超分工具.bat`。
3. 第一次使用先点软件左下角的 `安装/检查环境`。
4. 环境安装完成后，选择图片或文件夹，选择输出文件夹，然后开始超分。

如果电脑还没有 Python，双击启动脚本时会自动打开环境安装窗口。也可以直接双击 `安装运行环境.bat`。

## 轻量版包含什么

轻量包只包含程序源码、图形界面、安装脚本和说明文件。它不包含 Python 运行环境、模型权重和示例照片，所以下载体积很小。

第一次安装环境时会下载：

- Python 3.12：通过 winget 或 python.org 获取。
- CUDA 版 PyTorch：从 PyTorch 官方源获取。
- 其它 Python 依赖：从 Python 包源获取。
- 超分模型权重：第一次处理图片时自动下载到 `models` 文件夹。

## 主要功能

- 自动识别 NVIDIA 显卡型号、显存容量和当前空闲显存。
- 按显卡性能自动匹配更合适的处理占用。
- 默认使用 Transformer 超分模型。
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

本工具不是游戏里的原生 DLSS。游戏里的原生 DLSS 需要游戏引擎提供多帧、运动向量和深度信息；本工具处理的是单张图片或图片文件夹。
