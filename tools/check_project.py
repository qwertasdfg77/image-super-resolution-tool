#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md",
    "README.en.md",
    "FAQ.md",
    "CHANGELOG.md",
    "LICENSE",
    "SECURITY.md",
    "SUPPORT.md",
    "THIRD_PARTY_NOTICES.md",
    "RELEASE_DOWNLOAD.md",
    "install-from-github.ps1",
    "install-from-github.bat",
    "dlss_like_super_resolution.py",
    "dlss_like_super_resolution_gui.py",
    "start_gui.bat",
    "install_gpu.ps1",
    "install_gpu.bat",
    "docs/images/app-preview.png",
    "docs/images/before-after-demo.png",
    "docs/release-v1.0.0.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/python-check.yml",
]
REQUIRED_RELEASE_ASSETS = {
    "ImageSuperResolutionToolWebSetup.exe",
    "image-super-resolution-tool-full.zip.001",
    "image-super-resolution-tool-full.zip.002",
    "install-from-github.bat",
    "install-from-github.ps1",
    "merge-full-package.ps1",
    "SHA256.txt",
}


def fail(message: str) -> None:
    raise SystemExit(f"check failed: {message}")


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail("missing files: " + ", ".join(missing))


def check_readme_links() -> None:
    for md_name in ["README.md", "README.en.md", "RELEASE_DOWNLOAD.md", "FAQ.md", "docs/release-v1.0.0.md"]:
        text = (ROOT / md_name).read_text(encoding="utf-8")
        for match in re.finditer(r"\]\(([^)]+)\)", text):
            link = match.group(1)
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            if link.startswith("#"):
                continue
            local_path = (ROOT / md_name).parent / link
            if not local_path.exists():
                fail(f"{md_name} links to missing local path: {link}")


def check_installer_constants() -> None:
    text = (ROOT / "install-from-github.ps1").read_text(encoding="utf-8")
    for asset in ["image-super-resolution-tool-full.zip.001", "image-super-resolution-tool-full.zip.002"]:
        if asset not in text:
            fail(f"installer script does not reference {asset}")
    if "8CF07431598A6D9058689D912821887745CF10BC41F4F464F13054214F15E60B" not in text:
        fail("installer script is missing final package hash")


def check_release_assets() -> None:
    url = "https://api.github.com/repos/qwertasdfg77/image-super-resolution-tool/releases/tags/v1.0.0"
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    assets = {asset["name"] for asset in payload.get("assets", [])}
    missing = REQUIRED_RELEASE_ASSETS - assets
    if missing:
        fail("release is missing assets: " + ", ".join(sorted(missing)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-release", action="store_true", help="Skip GitHub Release asset check.")
    args = parser.parse_args()

    check_required_files()
    check_readme_links()
    check_installer_constants()
    if not args.skip_release:
        check_release_assets()
    print("project checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
