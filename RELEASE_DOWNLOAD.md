# 下载完整可运行包

完整可运行包包含 `.venv` 运行环境和模型权重，体积较大，因此放在 GitHub Release 附件中，不放入源码仓库。

## 推荐：一键安装器

下载并运行：

```text
ImageSuperResolutionToolWebSetup.exe
```

它会自动下载完整包、合并分卷、校验 SHA256、解压并创建快捷方式。

也可以下载脚本版一键安装器：

```text
install-from-github.bat
install-from-github.ps1
```

把这两个文件放在同一个文件夹，双击 `install-from-github.bat` 即可。

## 手动下载 3 步

1. 下载 Release 中的这些文件，并放到同一个文件夹：

- `image-super-resolution-tool-full.zip.001`
- `image-super-resolution-tool-full.zip.002`
- `merge-full-package.ps1`
- `SHA256.txt`

2. 在这个文件夹里打开 PowerShell，运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\merge-full-package.ps1
```

3. 等脚本合并出下面这个完整压缩包，解压后双击 `start_gui.bat` 使用：

```text
image-super-resolution-tool-full.zip
```

脚本会自动校验 SHA256。如果校验失败，请重新下载 `.001` 和 `.002` 分卷。

如果完整包里的运行环境在你的电脑上不可用，双击 `install_gpu.bat` 重新安装一次即可。
