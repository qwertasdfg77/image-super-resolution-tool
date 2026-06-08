## 图片超分辨率工具 v1.1.3 运行环境安装修复版

发布文件：

`ImageSuperResolutionTool-v1.1.3-Setup.exe`

## 本次修复

- 修复另一台电脑点击 `安装/检查环境` 后 Python 安装器运行结束但 `.python\python.exe` 缺失的问题。
- 本地 Python 运行时和 `.venv` 改为保存到当前用户的本地数据目录。
- Python 安装器失败时会自动重新下载并重试。
- 安装窗口会显示 Python 安装日志路径，便于继续排查。
- 启动脚本兼容新的运行环境目录，并保留旧 `.venv` 目录兼容。

## 使用方式

下载并双击 `ImageSuperResolutionTool-v1.1.3-Setup.exe`，选择安装位置。安装完成后，使用桌面快捷方式打开软件。

第一次打开软件后，点击左下角 `安装/检查环境` 安装本地 Python 运行时、CUDA 版 PyTorch 和其它依赖。
