# 图片超分辨率工具

Windows 图形界面图片超分工具。当前公开版本是 `v1.0.4` 含模型版，面向普通用户使用，不需要写代码。

## 下载

请到 Latest Release 下载：

- `ImageSuperResolutionTool-ModelIncluded.zip`：推荐，已经包含默认 Transformer 模型。
- `download-and-install.bat`：一键下载、解压并安装运行环境。
- `SHA256.txt`：用于校验下载文件。

Latest Release：
https://github.com/qwertasdfg77/image-super-resolution-tool/releases/latest

## 最简单用法

下载 `download-and-install.bat`，双击运行。它会自动：

1. 下载 `ImageSuperResolutionTool-ModelIncluded.zip` 到桌面。
2. 解压到桌面。
3. 打开环境安装流程。
4. 安装完成后打开图片超分辨率工具。

## 手动使用

1. 下载 `ImageSuperResolutionTool-ModelIncluded.zip`。
2. 解压到桌面或其它文件夹。
3. 双击 `打开超分工具.bat`。
4. 第一次使用先点软件左下角的 `安装/检查环境`。
5. 环境安装完成后，选择图片或文件夹，选择输出文件夹，然后开始超分。

## 这个版本包含什么

- 图形界面程序。
- 默认 Transformer 超分模型 `003_ATD_SRx4_finetune.pth`。
- 环境安装脚本。
- 中文使用说明。

这个版本不包含 `.venv` Python 运行环境，所以第一次安装环境时仍需要下载 Python、CUDA 版 PyTorch 和其它依赖。

## 主要功能

- 自动识别 NVIDIA 显卡型号、显存容量和当前空闲显存。
- 按显卡性能自动匹配更合适的处理占用。
- 默认使用 Transformer 超分模型。
- 默认模型已经内置，不需要首次联网下载模型。
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

GitHub 源码仓库不直接存放大体积 `.pth` 模型文件；公开下载包通过 Release 发布。

本工具不是游戏里的原生 DLSS。游戏里的原生 DLSS 需要游戏引擎提供多帧、运动向量和深度信息；本工具处理的是单张图片或图片文件夹。
