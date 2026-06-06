## 图片超分辨率工具 v1.0.1

这个版本重点优化公开下载和项目维护体验。程序核心超分逻辑与 v1.0.0 保持一致。

![界面预览](https://raw.githubusercontent.com/qwertasdfg77/image-super-resolution-tool/main/docs/images/app-preview.png)

![超分前后对比示意](https://raw.githubusercontent.com/qwertasdfg77/image-super-resolution-tool/main/docs/images/before-after-demo.png)

### 推荐：一键安装器

普通用户优先下载并运行：

```text
ImageSuperResolutionToolWebSetup.exe
```

它会自动下载完整包、合并分卷、校验 SHA256、解压并创建快捷方式。

v1.0.1 的安装器新增：

- 下载百分比
- 下载速度
- 预计剩余时间
- 下载失败自动重试

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

### v1.0.1 更新

- 优化一键联网安装器下载进度显示。
- 增加下载失败自动重试。
- 新增 Dependabot，自动关注 Python 依赖和 GitHub Actions 更新。
- 新增 CodeQL 安全扫描。
- 新增 Release check，用于检查安装器链接和 Release 附件完整性。

### 说明

完整包包含运行环境和模型权重，因体积较大拆成两个分卷上传。

本工具不是游戏里的原生 DLSS。原生 DLSS 需要游戏引擎提供多帧、运动向量和深度信息；本工具处理的是单张图片或图片文件夹。
