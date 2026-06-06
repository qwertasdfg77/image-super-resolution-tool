# Image Super Resolution Tool

A Windows GUI image upscaling tool. The current public release is `v1.0.3` Lightweight Edition.

## Download

Use the Latest Release page:

- `ImageSuperResolutionTool-Lightweight.zip`: recommended package.
- `download-lightweight.bat`: optional downloader that fetches and extracts the package.
- `SHA256.txt`: checksum file.

Latest Release:
https://github.com/qwertasdfg77/image-super-resolution-tool/releases/latest

## Usage

1. Extract `ImageSuperResolutionTool-Lightweight.zip`.
2. Double-click `打开超分工具.bat`.
3. On first use, click `安装/检查环境` in the app.
4. Select input image or folder, select output folder, then start upscaling.

The lightweight package does not include the Python environment, model weights, or sample photos. The app downloads required runtime files on the user's computer.

## Highlights

- NVIDIA GPU and VRAM detection.
- Automatic workload selection based on available GPU memory.
- Transformer super-resolution model support.
- Automatic sharpening and denoise settings.
- Percent progress bar with elapsed and estimated remaining time.
- Single image and folder batch processing.
- No saved previous input or output paths.
- No before/after preview panel in the app.

Recommended GPU: NVIDIA RTX 4060 8GB or higher.
