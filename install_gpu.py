#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
VENV_DIR = APP_DIR / ".venv"
VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
REQUIREMENTS = APP_DIR / "requirements.txt"


def run(command: list[str]) -> None:
    print()
    print(" ".join(command))
    subprocess.check_call(command, cwd=APP_DIR)


def ensure_supported_python() -> None:
    version = sys.version_info[:2]
    if version < (3, 10) or version > (3, 12):
        raise SystemExit("请使用 Python 3.10、3.11 或 3.12。推荐 Python 3.12。")


def ensure_venv() -> Path:
    if not VENV_PYTHON.exists():
        print(f"正在创建本地运行环境：{VENV_DIR}")
        run([sys.executable, "-m", "venv", str(VENV_DIR)])
    if not VENV_PYTHON.exists():
        raise SystemExit("本地 Python 环境创建失败。")
    return VENV_PYTHON


def main() -> int:
    ensure_supported_python()
    python = ensure_venv()

    print("正在安装/更新显卡运行环境。PyTorch CUDA 版体积较大，请耐心等待。")
    run([str(python), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(python), "-m", "pip", "install", "torch", "torchvision", "--index-url", "https://download.pytorch.org/whl/cu124"])
    run([str(python), "-m", "pip", "install", "-r", str(REQUIREMENTS)])

    print()
    print("正在检查 CUDA 和显卡...")
    run(
        [
            str(python),
            "-c",
            (
                "import torch; "
                "print('CUDA available:', torch.cuda.is_available()); "
                "print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'not found')"
            ),
        ]
    )
    print()
    print("完成。现在可以双击“打开超分工具.bat”启动软件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
