#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile


DEFAULT_REPO_URL = "https://github.com/Liang-HZ/network-fingerprint-audit.git"
DEFAULT_ZIP_URL = "https://codeload.github.com/Liang-HZ/network-fingerprint-audit/zip/refs/heads/main"


def run_command(args: list[str], cwd: pathlib.Path | None = None, timeout: int = 120) -> dict[str, object]:
    completed = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return {
        "args": args,
        "code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def command_available(name: str) -> bool:
    return shutil.which(name) is not None


def git_checkout(dest: pathlib.Path, repo_url: str, no_update: bool) -> tuple[bool, dict[str, object]]:
    if not command_available("git"):
        return False, {"code": None, "stderr": "git command not found"}
    if (dest / ".git").exists():
        if no_update:
            return True, {"code": 0, "stdout": "existing checkout reused"}
        result = run_command(["git", "pull", "--ff-only"], cwd=dest)
        return result["code"] == 0, result
    if dest.exists() and any(dest.iterdir()):
        return False, {"code": None, "stderr": f"destination exists and is not an empty git checkout: {dest}"}
    dest.parent.mkdir(parents=True, exist_ok=True)
    result = run_command(["git", "clone", "--depth", "1", repo_url, str(dest)])
    return result["code"] == 0, result


def zip_checkout(dest: pathlib.Path, zip_url: str) -> dict[str, object]:
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="network-audit-zip-") as tmp_raw:
        tmp = pathlib.Path(tmp_raw)
        archive = tmp / "repo.zip"
        urllib.request.urlretrieve(zip_url, archive)
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(tmp)
        extracted = next(path for path in tmp.iterdir() if path.is_dir())
        shutil.move(str(extracted), str(dest))
    return {"code": 0, "stdout": f"downloaded zip checkout to {dest}", "stderr": ""}


def ensure_repo(dest: pathlib.Path, repo_url: str, zip_url: str, no_update: bool) -> dict[str, object]:
    git_ok, git_result = git_checkout(dest, repo_url, no_update)
    if git_ok:
        return {"method": "git", "repo_path": str(dest), "detail": git_result}
    zip_result = zip_checkout(dest, zip_url)
    return {
        "method": "zip",
        "repo_path": str(dest),
        "detail": zip_result,
        "git_failure": git_result,
    }


def print_user_instructions(repo_dir: pathlib.Path) -> None:
    """Print copy-paste command for the user to run in their own Terminal."""
    collector_script = repo_dir / "network_audit.py"
    output_dir = repo_dir / "reports" / "agent-skill"
    user_cmd = f"python3 {collector_script} --output-dir {output_dir} --no-open"

    print(
        f"\n✅ 采集器仓库已下载完成，路径：{repo_dir}\n"
        f"\n"
        f"──────────────────────────────────────────────────────────\n"
        f"  请在 Claude Code 之外，打开一个新的终端窗口，粘贴\n"
        f"  下面这一行命令，按回车执行：\n"
        f"──────────────────────────────────────────────────────────\n"
        f"\n"
        f"  {user_cmd}\n"
        f"\n"
        f"──────────────────────────────────────────────────────────\n"
        f"\n"
        f"⏱  采集大约需要 1 分钟。执行完毕后，回到这个 Claude Code\n"
        f"   会话，告诉我「跑完了」，我会为你解读结果。\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch and run network-fingerprint-audit for agent interpretation.")
    parser.add_argument(
        "--dest",
        default=str(pathlib.Path.home() / ".cache" / "claude-code-trust-audit" / "network-fingerprint-audit"),
        help="Local checkout destination.",
    )
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL)
    parser.add_argument("--zip-url", default=DEFAULT_ZIP_URL)
    parser.add_argument("--no-update", action="store_true", help="Reuse an existing git checkout without pulling.")
    parser.add_argument("--skip-network", action="store_true")
    parser.add_argument("--skip-browser-probe", action="store_true")
    parser.add_argument("--default-browser-tracking-probe", action="store_true")
    parser.add_argument("--timeout", type=int, default=180)
    parsed = parser.parse_args()

    dest = pathlib.Path(parsed.dest).expanduser()
    ensure_repo(dest, parsed.repo_url, parsed.zip_url, parsed.no_update)
    print_user_instructions(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
