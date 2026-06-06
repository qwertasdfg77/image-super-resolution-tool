# 下载完整可运行包

完整可运行包包含 `.venv` 运行环境和模型权重，体积较大，因此放在 GitHub Release 附件中，不放入源码仓库。

下载 Release 中的这些文件：

- `image-super-resolution-tool-full.zip.001`
- `image-super-resolution-tool-full.zip.002`
- `merge-full-package.ps1`
- `SHA256.txt`

把这些文件放在同一个文件夹，右键 PowerShell 运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\merge-full-package.ps1
```

脚本会合并出：

```text
image-super-resolution-tool-full.zip
```

脚本会自动校验 SHA256。校验通过后，解压 ZIP，双击 `打开超分工具.bat` 即可使用。

如果完整包里的运行环境在你的电脑上不可用，双击 `安装运行环境.bat` 重新安装一次即可。
