# 第三方组件和模型说明

本项目会使用第三方开源库、模型结构和预训练模型权重。源码本身采用 MIT License；第三方组件和模型仍受各自上游许可证或使用条款约束。

## Python 依赖

| 名称 | 用途 | 上游链接 | 许可证信息 |
| --- | --- | --- | --- |
| PyTorch | CUDA 推理和张量计算 | https://github.com/pytorch/pytorch | 以 PyTorch 上游 LICENSE 为准 |
| torchvision | PyTorch 视觉相关依赖 | https://github.com/pytorch/vision | BSD-3-Clause |
| Pillow | 图片读取、保存和后处理 | https://github.com/python-pillow/Pillow | 以 Pillow 上游 LICENSE 为准 |
| NumPy | 数组和图片数据处理 | https://github.com/numpy/numpy | 以 NumPy 上游 LICENSE 为准 |
| Spandrel | 加载 Transformer/超分模型结构 | https://github.com/chaiNNer-org/spandrel | MIT |
| gdown | 从 Google Drive 下载模型权重 | https://github.com/wkentaro/gdown | MIT |
| packaging | Python 包版本处理 | https://github.com/pypa/packaging | 以 packaging 上游 LICENSE 为准 |

## 模型和算法

| 名称 | 用途 | 上游链接 | 许可证信息 |
| --- | --- | --- | --- |
| ATD / Adaptive Token Dictionary | 默认 Transformer 超分模型结构，程序默认使用 `003_ATD_SRx4_finetune` 权重 | https://github.com/CVL-UESTC/Adaptive-Token-Dictionary | Apache-2.0 |
| Real-ESRGAN | 照片和动漫备用超分模型 | https://github.com/xinntao/Real-ESRGAN | BSD-3-Clause |

## 重要说明

- 含模型版不包含 `.venv` 运行环境，但包含默认 Transformer 模型权重。
- 默认模型权重文件为 `models/003_ATD_SRx4_finetune.pth`，来源为 ATD / Adaptive Token Dictionary 项目相关发布资源。
- 如果你要重新分发完整包，请同时保留本文件、`LICENSE`、上游许可证链接，以及模型来源说明。
- 本项目不是 NVIDIA DLSS。DLSS 是游戏引擎内的多帧实时超采样技术；本项目处理的是单张图片或图片文件夹。
