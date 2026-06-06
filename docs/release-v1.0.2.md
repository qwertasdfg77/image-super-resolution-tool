## 图片超分辨率工具 v1.0.2

这个版本重点优化软件内使用体验，并处理 Dependabot 依赖更新。完整包仍然包含运行环境和模型权重。

![界面预览](https://raw.githubusercontent.com/qwertasdfg77/image-super-resolution-tool/main/docs/images/app-preview.png)

![超分前后对比示意](https://raw.githubusercontent.com/qwertasdfg77/image-super-resolution-tool/main/docs/images/before-after-demo.png)

### 推荐：一键安装器

普通用户优先下载并运行：

```text
ImageSuperResolutionToolWebSetup.exe
```

它会自动下载完整包、合并分卷、校验 SHA256、解压并创建快捷方式。

如果不想使用 EXE 安装器，也可以下载脚本版：

```text
install-from-github.bat
install-from-github.ps1
```

把这两个文件放在同一个文件夹，双击 `install-from-github.bat` 即可。

### 手动下载

也可以下载下面 4 个文件，并放到同一个文件夹：

- `image-super-resolution-tool-full.zip.001`
- `image-super-resolution-tool-full.zip.002`
- `merge-full-package.ps1`
- `SHA256.txt`

在这个文件夹里打开 PowerShell，运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\merge-full-package.ps1
```

脚本会生成 `image-super-resolution-tool-full.zip` 并自动校验 SHA256。解压后进入 `image-super-resolution-tool` 文件夹，双击 `start_gui.bat` 使用。

### v1.0.2 更新

- 软件内自动检查更新。
- 保存上次使用设置。
- 新增输出格式选择：自动、PNG、JPEG、WEBP。
- 新增 JPEG/WEBP 质量设置。
- 新增处理前后预览。
- 新增“打开输出文件夹”按钮。
- 合并 Dependabot 依赖更新。

### 说明

本工具不是游戏里的原生 DLSS。原生 DLSS 需要游戏引擎提供多帧、运动向量和深度信息；本工具处理的是单张图片或图片文件夹。
