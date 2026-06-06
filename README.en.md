# Image Super Resolution Tool

[![Python check](https://github.com/qwertasdfg77/image-super-resolution-tool/actions/workflows/python-check.yml/badge.svg)](https://github.com/qwertasdfg77/image-super-resolution-tool/actions/workflows/python-check.yml)
[![CodeQL](https://github.com/qwertasdfg77/image-super-resolution-tool/actions/workflows/codeql.yml/badge.svg)](https://github.com/qwertasdfg77/image-super-resolution-tool/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/github/license/qwertasdfg77/image-super-resolution-tool)](LICENSE)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D4)
![CUDA](https://img.shields.io/badge/NVIDIA-CUDA-76B900)
![Transformer](https://img.shields.io/badge/Model-Transformer-4F46E5)

Windows GUI image super-resolution tool with NVIDIA CUDA auto-tuning, transformer model support, automatic sharpening, and automatic denoise.

Chinese README: [README.md](README.md)

![App preview](docs/images/app-preview.png)

![Before and after demo](docs/images/before-after-demo.png)

## Recommended Download

Open the [v1.0.2 release page](https://github.com/qwertasdfg77/image-super-resolution-tool/releases/tag/v1.0.2) and download:

```text
ImageSuperResolutionToolWebSetup.exe
```

Run it to automatically download the full package, merge split parts, verify SHA256, extract the tool, and create shortcuts.

If you prefer manual installation, download these 4 files into the same folder:

- `image-super-resolution-tool-full.zip.001`
- `image-super-resolution-tool-full.zip.002`
- `merge-full-package.ps1`
- `SHA256.txt`

Open PowerShell in that folder and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\merge-full-package.ps1
```

Extract `image-super-resolution-tool-full.zip`, enter the `image-super-resolution-tool` folder, then double-click `start_gui.bat`.

If the included runtime does not work on your computer, run `install_gpu.bat` once to reinstall the Python/CUDA environment.

## Features

- No-code Windows GUI.
- Automatic NVIDIA GPU, CUDA, and VRAM detection.
- Automatic tile size, memory usage, and precision tuning.
- Default ATD x4 Transformer model.
- Real-ESRGAN photo and anime fallback models.
- Automatic sharpening and denoise.
- Output format selection: auto, PNG, JPEG, WEBP.
- JPEG/WEBP quality setting.
- Before/after preview, output-folder shortcut, saved settings, and update check.
- Percentage progress bar with elapsed time and ETA.
- Single image and folder batch processing.

## Notes

This is not native in-game NVIDIA DLSS. DLSS needs engine-side motion vectors, depth, and multi-frame data. This tool processes still images or image folders.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for third-party components and model information.
