# 更新记录

## v1.0.1 - 2026-06-06

公开分发体验增强版。

- 优化一键联网安装器下载体验：显示百分比、下载速度和预计剩余时间。
- 下载失败时自动重试，减少大文件下载中断带来的手动操作。
- 新增 Dependabot 配置，自动关注 Python 依赖和 GitHub Actions 更新。
- 新增 CodeQL 安全扫描 workflow。
- 新增独立 Release check workflow，用于检查安装器链接和 Release 附件完整性。
- README 和英文 README 增加 CodeQL 状态徽章。

## v1.0.0 后续公开仓库优化 - 2026-06-06

- 新增一键联网安装脚本和正式安装包脚本。
- 新增 FAQ 常见问题。
- 新增 README 英文摘要、第三方组件说明、支持说明和安全说明。
- 增强 GitHub Actions 自动检查：GUI 导入、安装器链接、README 图片和 Release 必要附件。

## v1.0.0 - 2026-06-06

首次公开发布。

- 提供 Windows 图形界面，无需写代码即可使用。
- 支持 NVIDIA CUDA 显卡检测和显存自动匹配。
- 默认使用 ATD x4 Transformer 超分模型。
- 支持 Real-ESRGAN 照片和动漫备用模型。
- 支持自动锐化、自动去噪、单图处理和文件夹批量处理。
- 增加百分比进度条、已用时间和预计剩余时间显示。
- 提供 GitHub Release 完整可运行包，包含运行环境和模型权重。
