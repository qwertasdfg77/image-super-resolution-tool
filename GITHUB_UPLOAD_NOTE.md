# GitHub 上传说明

这个文件夹是适合上传到 GitHub 的源码版。

已包含：

- 图形界面源码
- 超分核心源码
- Windows 启动脚本
- Windows 安装脚本
- Python 依赖文件
- 使用说明

未包含：

- `.venv` 运行环境
- `models/*.pth` 模型权重

原因：

- `.venv` 体积约数 GB，不适合放入 GitHub 仓库。
- ATD Transformer 模型权重约 164MB，超过 GitHub 普通仓库单文件限制。
- 程序首次运行时会自动下载模型，安装脚本会自动创建运行环境。

如果要完整分发可运行版本，建议用压缩包或 GitHub Release，而不是直接提交 `.venv` 和模型到源码仓库。
