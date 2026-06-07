# 第三方组件和模型说明

本项目会使用第三方开源库、模型结构和预训练模型权重。源码本身采用 MIT License；第三方组件和模型仍受各自上游许可证或使用条款约束。

## Python 依赖

| 名称 | 用途 | 上游链接 | 许可证信息 |
| --- | --- | --- | --- |
| PyTorch | CUDA 推理和张量计算 | https://github.com/pytorch/pytorch | 以 PyTorch 上游 LICENSE 为准 |
| torchvision | PyTorch 视觉相关依赖 | https://github.com/pytorch/vision | BSD-3-Clause |
| Spandrel | 加载 ATD 和 HAT Transformer 模型 | https://github.com/chaiNNer-org/spandrel | MIT |
| safetensors | Spandrel 依赖的安全权重文件读取库 | https://github.com/huggingface/safetensors | Apache-2.0 |
| Pillow | 图片读取、保存和后处理 | https://github.com/python-pillow/Pillow | 以 Pillow 上游 LICENSE 为准 |
| NumPy | 数组和图片数据处理 | https://github.com/numpy/numpy | 以 NumPy 上游 LICENSE 为准 |
| packaging | Python 包版本处理 | https://github.com/pypa/packaging | 以 packaging 上游 LICENSE 为准 |

## 模型和算法

| 名称 | 用途 | 上游链接 | 许可证信息 |
| --- | --- | --- | --- |
| ATD | 官方超分辨率模型 | https://github.com/LabShuHangGU/Adaptive-Token-Dictionary | Apache-2.0 |
| HAT | 高质量超分辨率模型 | https://github.com/XPixelGroup/HAT | Apache-2.0 |
| Real-ESRGAN | 通用照片和动漫插画超分模型 | https://github.com/xinntao/Real-ESRGAN | BSD-3-Clause |

## 包内模型

- `models/003_ATD_SRx4_finetune.pth`
- `models/Real_HAT_GAN_sharper.pth`
- `models/RealESRGAN_x4plus.pth`
- `models/RealESRGAN_x4plus_anime_6B.pth`

ATD 权重来自 ATD 官方预训练模型，OpenModelDB 标注 SHA256 为 `092bf6aa82f0ecb9f681a7da6a8e65e2c1280ae5b44f1608f60742d88547b833`。HAT 权重来自公开镜像仓库 `Acly/hat`。重新分发本项目时请同时保留本文件、`LICENSE`、上游许可证链接和模型来源说明。

本项目不是 NVIDIA DLSS。DLSS 是游戏引擎内的多帧实时超采样技术；本项目处理的是单张图片或图片文件夹。
