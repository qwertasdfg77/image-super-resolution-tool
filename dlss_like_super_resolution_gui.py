#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import queue
import json
import re
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path
from tkinter import BooleanVar, DoubleVar, IntVar, StringVar, Text, Tk, filedialog, messagebox
from tkinter import ttk

CURRENT_VERSION = "v1.0.3"
APP_DIR = Path(__file__).resolve().parent
ENGINE_SCRIPT = APP_DIR / "dlss_like_super_resolution.py"
INSTALL_SCRIPT = APP_DIR / "install_gpu.bat"
SETTINGS_DIR = Path(os.environ.get("APPDATA", APP_DIR)) / "ImageSuperResolutionTool"
SETTINGS_PATH = SETTINGS_DIR / "settings.json"
LATEST_RELEASE_API = "https://api.github.com/repos/qwertasdfg77/image-super-resolution-tool/releases/latest"
RELEASES_URL = "https://github.com/qwertasdfg77/image-super-resolution-tool/releases/latest"

MODEL_OPTIONS = {
    "ATD Transformer 自动推荐": "transformer",
    "Real-ESRGAN 照片备用": "photo",
    "Real-ESRGAN 动漫备用": "anime",
}

GPU_USAGE_OPTIONS = {
    "自动": "auto",
    "保守": "conservative",
    "均衡": "balanced",
    "性能": "performance",
}

OUTPUT_FORMAT_OPTIONS = {
    "自动": "auto",
    "PNG": "png",
    "JPEG": "jpeg",
    "WEBP": "webp",
}


def runtime_python() -> str:
    venv_python = APP_DIR / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    exe = Path(sys.executable)
    if exe.name.lower() == "pythonw.exe":
        console_python = exe.with_name("python.exe")
        if console_python.exists():
            return str(console_python)
    return str(exe)


def format_duration(seconds: float | None) -> str:
    if seconds is None or seconds < 0:
        return "--:--"
    seconds = int(round(seconds))
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def load_settings() -> dict:
    try:
        if SETTINGS_PATH.exists():
            return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {}


def save_settings(data: dict) -> None:
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def choice_setting(settings: dict, key: str, default: str, choices: dict[str, str]) -> str:
    value = settings.get(key, default)
    return value if value in choices else default


def int_setting(settings: dict, key: str, default: int, minimum: int, maximum: int) -> int:
    try:
        value = int(settings.get(key, default))
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, value))


def version_tuple(tag: str) -> tuple[int, ...]:
    numbers = re.findall(r"\d+", tag)
    return tuple(int(part) for part in numbers[:3]) or (0,)


def is_newer_version(latest: str, current: str) -> bool:
    return version_tuple(latest) > version_tuple(current)


class SuperResolutionApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title(f"图片超分辨率工具 {CURRENT_VERSION}")
        self.root.geometry("1080x760")
        self.root.minsize(940, 680)

        settings = load_settings()
        self.settings_ready = False
        self.input_path = StringVar(value="")
        self.output_path = StringVar(value="")
        self.model_display = StringVar(value=choice_setting(settings, "model_display", "ATD Transformer 自动推荐", MODEL_OPTIONS))
        self.scale = StringVar(value=str(settings.get("scale", "4")) if str(settings.get("scale", "4")) in {"2", "3", "4"} else "4")
        self.gpu_usage_display = StringVar(value=choice_setting(settings, "gpu_usage_display", "自动", GPU_USAGE_OPTIONS))
        self.output_format_display = StringVar(value=choice_setting(settings, "output_format_display", "自动", OUTPUT_FORMAT_OPTIONS))
        self.jpeg_quality = IntVar(value=int_setting(settings, "jpeg_quality", 95, 1, 100))
        self.auto_sharpness = BooleanVar(value=bool(settings.get("auto_sharpness", True)))
        self.auto_denoise = BooleanVar(value=bool(settings.get("auto_denoise", True)))
        self.sharpness = DoubleVar(value=float(settings.get("sharpness", 0.65)))
        self.denoise = DoubleVar(value=float(settings.get("denoise", 0.06)))
        self.tta = BooleanVar(value=bool(settings.get("tta", False)))
        self.quiet = BooleanVar(value=bool(settings.get("quiet", False)))
        self.status = StringVar(value="请选择图片或文件夹")
        self.progress_text = StringVar(value="进度：0% | 已用 00:00 | 剩余 --:--")

        self.process: subprocess.Popen | None = None
        self.log_queue: queue.Queue[str] = queue.Queue()
        self.sharpness_slider: ttk.Scale | None = None
        self.denoise_slider: ttk.Scale | None = None
        self.run_started_at: float | None = None
        self.last_eta: float | None = None
        self.last_percent = 0.0
        self.last_output_path: Path | None = None

        self.build_ui()
        self.auto_sharpness.trace_add("write", lambda *_: self.update_slider_state())
        self.auto_denoise.trace_add("write", lambda *_: self.update_slider_state())
        for var in (
            self.model_display,
            self.scale,
            self.gpu_usage_display,
            self.output_format_display,
            self.jpeg_quality,
            self.auto_sharpness,
            self.auto_denoise,
            self.sharpness,
            self.denoise,
            self.tta,
            self.quiet,
        ):
            var.trace_add("write", lambda *_: self.save_current_settings())
        self.settings_ready = True
        if "input_path" in settings or "output_path" in settings:
            self.save_current_settings()
        self.update_slider_state()
        self.root.after(120, self.drain_log_queue)
        self.root.after(1000, self.update_elapsed_clock)
        self.root.after(1800, lambda: self.check_updates(manual=False))
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.check_environment(silent=True)

    def build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main = ttk.Frame(self.root, padding=18)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(5, weight=1)

        ttk.Label(main, text="图片超分辨率工具", font=("Microsoft YaHei UI", 17, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(main, textvariable=self.status).grid(row=1, column=0, sticky="w", pady=(4, 14))

        paths = ttk.LabelFrame(main, text="图片")
        paths.grid(row=2, column=0, sticky="ew")
        paths.columnconfigure(1, weight=1)

        ttk.Button(paths, text="选择图片", command=self.choose_file).grid(row=0, column=0, padx=10, pady=(12, 6), sticky="ew")
        ttk.Entry(paths, textvariable=self.input_path).grid(row=0, column=1, padx=(0, 10), pady=(12, 6), sticky="ew")
        ttk.Button(paths, text="选择文件夹", command=self.choose_folder).grid(row=0, column=2, padx=(0, 10), pady=(12, 6), sticky="ew")

        ttk.Button(paths, text="输出位置", command=self.choose_output).grid(row=1, column=0, padx=10, pady=(0, 12), sticky="ew")
        ttk.Entry(paths, textvariable=self.output_path).grid(row=1, column=1, columnspan=2, padx=(0, 10), pady=(0, 12), sticky="ew")

        options = ttk.LabelFrame(main, text="效果")
        options.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        for col in range(5):
            options.columnconfigure(col, weight=1)

        ttk.Label(options, text="模型").grid(row=0, column=0, padx=10, pady=(12, 4), sticky="w")
        ttk.Combobox(
            options,
            textvariable=self.model_display,
            values=tuple(MODEL_OPTIONS),
            state="readonly",
            width=22,
        ).grid(row=1, column=0, padx=10, pady=(0, 12), sticky="ew")

        ttk.Label(options, text="放大倍数").grid(row=0, column=1, padx=10, pady=(12, 4), sticky="w")
        ttk.Combobox(options, textvariable=self.scale, values=("2", "3", "4"), state="readonly", width=10).grid(
            row=1, column=1, padx=10, pady=(0, 12), sticky="ew"
        )

        ttk.Label(options, text="显卡占用").grid(row=0, column=2, padx=10, pady=(12, 4), sticky="w")
        ttk.Combobox(
            options,
            textvariable=self.gpu_usage_display,
            values=tuple(GPU_USAGE_OPTIONS),
            state="readonly",
            width=10,
        ).grid(row=1, column=2, padx=10, pady=(0, 12), sticky="ew")

        ttk.Checkbutton(options, text="更高质量", variable=self.tta).grid(row=1, column=3, padx=10, pady=(0, 12), sticky="w")
        ttk.Checkbutton(options, text="简洁日志", variable=self.quiet).grid(row=1, column=4, padx=10, pady=(0, 12), sticky="w")

        ttk.Label(options, text="输出格式").grid(row=2, column=0, padx=10, pady=(0, 4), sticky="w")
        ttk.Combobox(
            options,
            textvariable=self.output_format_display,
            values=tuple(OUTPUT_FORMAT_OPTIONS),
            state="readonly",
            width=10,
        ).grid(row=3, column=0, padx=10, pady=(0, 12), sticky="ew")

        ttk.Label(options, text="JPEG/WEBP 质量").grid(row=2, column=1, padx=10, pady=(0, 4), sticky="w")
        ttk.Spinbox(options, from_=1, to=100, textvariable=self.jpeg_quality, width=10).grid(
            row=3, column=1, padx=10, pady=(0, 12), sticky="ew"
        )

        post = ttk.LabelFrame(main, text="自动锐化和去噪")
        post.grid(row=4, column=0, sticky="ew", pady=(14, 0))
        post.columnconfigure(2, weight=1)
        post.columnconfigure(5, weight=1)

        ttk.Checkbutton(post, text="自动锐化", variable=self.auto_sharpness).grid(row=0, column=0, padx=10, pady=12, sticky="w")
        ttk.Label(post, text="手动锐化").grid(row=0, column=1, padx=(4, 10), pady=12, sticky="w")
        self.sharpness_slider = ttk.Scale(post, variable=self.sharpness, from_=0, to=1.5, orient="horizontal")
        self.sharpness_slider.grid(row=0, column=2, padx=(0, 18), pady=12, sticky="ew")

        ttk.Checkbutton(post, text="自动去噪", variable=self.auto_denoise).grid(row=0, column=3, padx=10, pady=12, sticky="w")
        ttk.Label(post, text="手动去噪").grid(row=0, column=4, padx=(4, 10), pady=12, sticky="w")
        self.denoise_slider = ttk.Scale(post, variable=self.denoise, from_=0, to=0.3, orient="horizontal")
        self.denoise_slider.grid(row=0, column=5, padx=(0, 10), pady=12, sticky="ew")

        log_frame = ttk.LabelFrame(main, text="运行状态")
        log_frame.grid(row=5, column=0, sticky="nsew", pady=(14, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log = Text(log_frame, height=9, wrap="word", state="disabled")
        self.log.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        scroll = ttk.Scrollbar(log_frame, command=self.log.yview)
        scroll.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)
        self.log.configure(yscrollcommand=scroll.set)

        actions = ttk.Frame(main)
        actions.grid(row=6, column=0, sticky="ew", pady=(14, 0))
        actions.columnconfigure(4, weight=1)

        ttk.Button(actions, text="安装/检查环境", command=self.open_installer).grid(row=0, column=0, padx=(0, 10), sticky="w")
        ttk.Button(actions, text="检测显卡", command=lambda: self.check_environment(silent=False)).grid(row=0, column=1, padx=(0, 10), sticky="w")
        ttk.Button(actions, text="检查更新", command=lambda: self.check_updates(manual=True)).grid(row=0, column=2, padx=(0, 10), sticky="w")
        self.open_output_button = ttk.Button(actions, text="打开输出文件夹", command=self.open_output_folder, state="disabled")
        self.open_output_button.grid(row=0, column=3, padx=(0, 10), sticky="w")
        self.progress = ttk.Progressbar(actions, mode="determinate", maximum=100, value=0)
        self.progress.grid(row=0, column=4, padx=10, sticky="ew")
        ttk.Label(actions, textvariable=self.progress_text).grid(row=1, column=4, padx=10, pady=(4, 0), sticky="ew")
        self.stop_button = ttk.Button(actions, text="停止", command=self.stop_run, state="disabled")
        self.stop_button.grid(row=0, column=5, padx=(10, 0), sticky="e")
        self.start_button = ttk.Button(actions, text="开始超分", command=self.start_run)
        self.start_button.grid(row=0, column=6, padx=(10, 0), sticky="e")

        self.append_log("使用顺序：先安装/检查环境，再选择图片，最后点“开始超分”。")
        self.append_log("程序会自动识别显卡型号和显存，并自动匹配 tile、精度和显存占用。")

    def update_slider_state(self) -> None:
        if self.sharpness_slider:
            self.sharpness_slider.configure(state="disabled" if self.auto_sharpness.get() else "normal")
        if self.denoise_slider:
            self.denoise_slider.configure(state="disabled" if self.auto_denoise.get() else "normal")

    def save_current_settings(self) -> None:
        if not getattr(self, "settings_ready", False):
            return
        try:
            save_settings(
                {
                    "model_display": self.model_display.get(),
                    "scale": self.scale.get(),
                    "gpu_usage_display": self.gpu_usage_display.get(),
                    "output_format_display": self.output_format_display.get(),
                    "jpeg_quality": self.current_jpeg_quality(),
                    "auto_sharpness": self.auto_sharpness.get(),
                    "auto_denoise": self.auto_denoise.get(),
                    "sharpness": self.sharpness.get(),
                    "denoise": self.denoise.get(),
                    "tta": self.tta.get(),
                    "quiet": self.quiet.get(),
                }
            )
        except Exception:
            pass

    def current_jpeg_quality(self) -> int:
        try:
            value = int(self.jpeg_quality.get())
        except Exception:
            return 95
        return max(1, min(100, value))

    def on_close(self) -> None:
        self.save_current_settings()
        self.root.destroy()

    def choose_file(self) -> None:
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[
                ("图片", "*.jpg *.jpeg *.png *.webp *.bmp *.tif *.tiff"),
                ("所有文件", "*.*"),
            ],
        )
        if path:
            self.input_path.set(path)
            self.output_path.set(str(Path(path).parent / "upscaled"))

    def choose_folder(self) -> None:
        path = filedialog.askdirectory(title="选择图片文件夹")
        if path:
            self.input_path.set(path)
            self.output_path.set(str(Path(path) / "upscaled"))

    def choose_output(self) -> None:
        path = filedialog.askdirectory(title="选择输出文件夹")
        if path:
            self.output_path.set(path)

    def open_output_folder(self) -> None:
        output = Path(self.output_path.get()) if self.output_path.get() else None
        if self.last_output_path and self.last_output_path.exists():
            folder = self.last_output_path.parent
        elif output and output.suffix:
            folder = output.parent
        elif output:
            folder = output
        else:
            messagebox.showwarning("缺少输出位置", "还没有可打开的输出文件夹。")
            return
        if not folder.exists():
            messagebox.showwarning("文件夹不存在", f"找不到输出文件夹：{folder}")
            return
        os.startfile(folder)

    def append_log(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", text.rstrip() + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def parse_engine_path(self, text: str, prefix: str) -> Path | None:
        if not text.startswith(prefix):
            return None
        value = text[len(prefix) :].split(" (", 1)[0].strip()
        return Path(value) if value else None

    def handle_engine_log(self, text: str) -> None:
        output_path = self.parse_engine_path(text, "Output: ")
        if output_path is not None:
            self.last_output_path = output_path
            self.open_output_button.configure(state="normal")
        self.append_log(text)

    def reset_progress(self) -> None:
        self.last_percent = 0.0
        self.last_eta = None
        self.progress.configure(value=0)
        self.progress_text.set("进度：0% | 已用 00:00 | 剩余 --:--")

    def handle_progress_message(self, item: str) -> None:
        parts = item.split("|")
        if len(parts) != 5:
            return
        try:
            current = int(parts[1])
            total = max(1, int(parts[2]))
            elapsed = float(parts[3])
            eta = float(parts[4])
        except ValueError:
            return
        percent = max(0.0, min(100.0, current / total * 100))
        self.last_percent = percent
        self.last_eta = eta
        self.progress.configure(value=percent)
        self.progress_text.set(
            f"进度：{percent:.0f}% | 已用 {format_duration(elapsed)} | 剩余 {format_duration(eta)}"
        )

    def update_elapsed_clock(self) -> None:
        if self.process is not None and self.run_started_at is not None:
            elapsed = time.monotonic() - self.run_started_at
            self.progress_text.set(
                f"进度：{self.last_percent:.0f}% | 已用 {format_duration(elapsed)} | 剩余 {format_duration(self.last_eta)}"
            )
        self.root.after(1000, self.update_elapsed_clock)

    def drain_log_queue(self) -> None:
        while True:
            try:
                item = self.log_queue.get_nowait()
            except queue.Empty:
                break
            if item.startswith("__DONE__:"):
                self.finish_run(int(item.split(":", 1)[1]))
            elif item.startswith("__PROGRESS__|"):
                self.handle_progress_message(item)
            else:
                self.handle_engine_log(item)
        self.root.after(120, self.drain_log_queue)

    def build_command(self) -> list[str]:
        sharpness = "auto" if self.auto_sharpness.get() else f"{self.sharpness.get():.2f}"
        denoise = "auto" if self.auto_denoise.get() else f"{self.denoise.get():.2f}"
        command = [
            runtime_python(),
            str(ENGINE_SCRIPT),
            self.input_path.get(),
            "-o",
            self.output_path.get(),
            "--model",
            MODEL_OPTIONS[self.model_display.get()],
            "--outscale",
            self.scale.get(),
            "--output-format",
            OUTPUT_FORMAT_OPTIONS[self.output_format_display.get()],
            "--gpu-usage",
            GPU_USAGE_OPTIONS[self.gpu_usage_display.get()],
            "--tile",
            "auto",
            "--tile-pad",
            "auto",
            "--precision",
            "auto",
            "--model-dir",
            str(APP_DIR / "models"),
            "--sharpness",
            sharpness,
            "--denoise",
            denoise,
            "--jpeg-quality",
            str(self.current_jpeg_quality()),
        ]
        if self.tta.get():
            command.append("--tta")
        if self.quiet.get():
            command.append("--quiet")
        return command

    def start_run(self) -> None:
        if self.process is not None:
            return
        if not self.input_path.get():
            messagebox.showwarning("缺少图片", "请先选择图片或图片文件夹。")
            return
        if not self.output_path.get():
            messagebox.showwarning("缺少输出位置", "请先选择输出文件夹。")
            return
        if not ENGINE_SCRIPT.exists():
            messagebox.showerror("文件缺失", f"找不到主程序：{ENGINE_SCRIPT}")
            return

        self.save_current_settings()
        self.append_log("")
        self.append_log("开始处理...")
        self.status.set("正在使用显卡超分，请等待")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.reset_progress()
        self.run_started_at = time.monotonic()
        self.last_output_path = None

        threading.Thread(target=self.run_process, args=(self.build_command(),), daemon=True).start()

    def run_process(self, command: list[str]) -> None:
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        try:
            self.process = subprocess.Popen(
                command,
                cwd=str(APP_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=flags,
            )
            assert self.process.stdout is not None
            for line in self.process.stdout:
                self.log_queue.put(line.rstrip())
            code = self.process.wait()
        except Exception as exc:
            self.log_queue.put(f"启动失败：{exc}")
            code = 1
        self.log_queue.put(f"__DONE__:{code}")

    def finish_run(self, code: int) -> None:
        elapsed = time.monotonic() - self.run_started_at if self.run_started_at is not None else 0.0
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.process = None
        if code == 0:
            self.progress.configure(value=100)
            self.progress_text.set(f"进度：100% | 已用 {format_duration(elapsed)} | 剩余 00:00")
            self.status.set("完成")
            self.append_log("处理完成。")
            messagebox.showinfo("完成", "图片超分已经完成。")
        else:
            self.status.set("未完成")
            self.progress_text.set(
                f"进度：{self.last_percent:.0f}% | 已用 {format_duration(elapsed)} | 剩余 --:--"
            )
            self.append_log("处理未完成，请查看上面的运行状态。")
            messagebox.showerror("未完成", "处理未完成，请查看运行状态。")
        self.run_started_at = None

    def stop_run(self) -> None:
        if self.process is None:
            return
        self.append_log("正在停止...")
        self.process.terminate()

    def check_updates(self, manual: bool) -> None:
        def worker() -> None:
            try:
                request = urllib.request.Request(
                    LATEST_RELEASE_API,
                    headers={"User-Agent": f"ImageSuperResolutionTool/{CURRENT_VERSION}"},
                )
                with urllib.request.urlopen(request, timeout=12) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                latest_tag = payload.get("tag_name", "")
                latest_url = payload.get("html_url", RELEASES_URL)
                if latest_tag and is_newer_version(latest_tag, CURRENT_VERSION):
                    def notify() -> None:
                        self.status.set(f"发现新版本：{latest_tag}")
                        self.append_log(f"发现新版本：{latest_tag}，当前版本：{CURRENT_VERSION}")
                        if messagebox.askyesno("发现新版本", f"发现新版本 {latest_tag}，是否打开下载页面？"):
                            webbrowser.open(latest_url)

                    self.root.after(0, notify)
                elif manual:
                    self.root.after(0, lambda: messagebox.showinfo("检查更新", f"当前已经是最新版本：{CURRENT_VERSION}"))
            except Exception as exc:
                if manual:
                    message = str(exc)
                    self.root.after(0, lambda: messagebox.showwarning("检查更新失败", message))

        threading.Thread(target=worker, daemon=True).start()

    def open_installer(self) -> None:
        if not INSTALL_SCRIPT.exists():
            messagebox.showerror("文件缺失", f"找不到安装脚本：{INSTALL_SCRIPT}")
            return
        try:
            os.startfile(INSTALL_SCRIPT)
        except Exception as exc:
            messagebox.showerror("无法打开安装器", str(exc))

    def check_environment(self, silent: bool) -> None:
        def worker() -> None:
            command = [
                runtime_python(),
                "-c",
                (
                    "import sys\n"
                    "print('Python:', sys.executable)\n"
                    "try:\n"
                    "    import torch\n"
                    "    print('PyTorch:', torch.__version__)\n"
                    "    print('CUDA:', torch.cuda.is_available())\n"
                    "    if torch.cuda.is_available():\n"
                    "        props = torch.cuda.get_device_properties(0)\n"
                    "        free, total = torch.cuda.mem_get_info(0)\n"
                    "        print('GPU:', torch.cuda.get_device_name(0))\n"
                    "        print('VRAM:', round(total / 1024**3, 1), 'GB')\n"
                    "        print('Free VRAM:', round(free / 1024**3, 1), 'GB')\n"
                    "        print('SM:', getattr(props, 'multi_processor_count', 0))\n"
                    "except Exception as e:\n"
                    "    print('PyTorch/CUDA check failed:', e)\n"
                ),
            ]
            flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            result = subprocess.run(
                command,
                cwd=str(APP_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=flags,
            )
            output = result.stdout.strip()
            if not silent:
                self.log_queue.put("")
                for line in output.splitlines():
                    self.log_queue.put(line)
            if "CUDA: True" in output:
                gpu_line = next((line for line in output.splitlines() if line.startswith("GPU:")), "GPU: 已检测到显卡")
                self.root.after(0, lambda: self.status.set(gpu_line))
            elif not silent:
                self.root.after(
                    0,
                    lambda: messagebox.showwarning("需要安装环境", "没有检测到可用 CUDA 环境，请先点击“安装/检查环境”。"),
                )

        threading.Thread(target=worker, daemon=True).start()


def main() -> None:
    root = Tk()
    try:
        style = ttk.Style(root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    SuperResolutionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
