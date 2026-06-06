## 图片超分辨率工具 v1.0.0

Windows 图形界面图片超分工具，支持 NVIDIA CUDA 显卡自动识别、显存自动匹配、ATD Transformer 超分模型、自动锐化和自动去噪。

![界面预览](https://raw.githubusercontent.com/qwertasdfg77/image-super-resolution-tool/main/docs/images/app-preview.png)

![超分前后对比示意](https://raw.githubusercontent.com/qwertasdfg77/image-super-resolution-tool/main/docs/images/before-after-demo.png)

### 新手下载 3 步

1. 下载下面 4 个文件，并放到同一个文件夹：
   - `image-super-resolution-tool-full.zip.001`
   - `image-super-resolution-tool-full.zip.002`
   - `merge-full-package.ps1`
   - `SHA256.txt`
2. 在这个文件夹里打开 PowerShell，运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\merge-full-package.ps1
```

3. 等脚本生成 `image-super-resolution-tool-full.zip`，解压后进入 `image-super-resolution-tool` 文件夹，双击 `start_gui.bat` 使用。

如果完整包里的运行环境在你的电脑上不可用，双击 `install_gpu.bat` 重新安装一次即可。

### 主要功能

- 无需写代码，双击运行。
- 自动识别 NVIDIA 显卡型号、显存容量和当前空闲显存。
- 默认使用 ATD x4 Transformer 模型。
- 支持 Real-ESRGAN 照片/动漫备用模型。
- 自动锐化和自动去噪。
- 百分比进度条，显示已用时间和预计剩余时间。
- 支持单张图片和整个文件夹批量处理。

### 说明

完整包包含运行环境和模型权重，因体积较大拆成两个分卷上传。

本工具不是游戏里的原生 DLSS。原生 DLSS 需要游戏引擎提供多帧、运动向量和深度信息；本工具处理的是单张图片或图片文件夹。
