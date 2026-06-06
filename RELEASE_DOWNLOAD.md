# 下载完整可运行包

完整可运行包包含 `.venv` 运行环境和模型权重，体积较大，因此放在 GitHub Release 附件中，不放入源码仓库。

下载 Release 中的这些文件：

- `图片超分辨率工具-full.zip.001`
- `图片超分辨率工具-full.zip.002`
- `合并完整包.ps1`
- `完整包校验_SHA256.txt`

把这些文件放在同一个文件夹，右键 PowerShell 运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\合并完整包.ps1
```

脚本会合并出：

```text
图片超分辨率工具-full.zip
```

解压后双击 `打开超分工具.bat` 即可使用。
