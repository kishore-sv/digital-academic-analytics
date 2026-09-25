#!/usr/bin/env python3
"""
Cross-platform project setup for ScholarPulse (macOS, Linux, Windows).

After cloning:
  python setup.py              # install deps, DB, migrate, seed
  python setup.py --start      # same + run API and client dev servers

Requires: Python 3.13+, Docker, uv, Bun (install hints printed if missing).
"""

from __future__ import annotations

import argparse
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
CLIENT = ROOT / "client"
ML = ROOT / "ml"

MIN_PYTHON = (3, 13)
POSTGRES_IMAGE = "postgres:16"
POSTGRES_CONTAINER = "prj649_postgres"
POSTGRES_USER = "prj649"


def _is_windows() -> bool:
    return sys.platform == "win32"


def _run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    print(f"\n→ {' '.join(cmd)}")
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        env=merged,
        check=check,
        text=True,
    )


def _which(name: str) -> str | None:
    return shutil.which(name)


def _require_tools() -> None:
    missing: list[str] = []
    if not _which("docker"):
        missing.append("Docker — https://docs.docker.com/get-docker/")
    if not _which("uv"):
        missing.append(
            "uv — https://docs.astral.sh/uv/getting-started/installation/\n"
            "    macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh\n"
            "    Windows: powershell -ExecutionPolicy ByPass -c "
            '"irm https://astral.sh/uv/install.ps1 | iex"'
        )
    if not _which("bun"):
        missing.append("Bun — https://bun.sh/docs/installation")
    if missing:
        print("Missing required tools:\n")
        for item in missing:
            print(f"  • {item}")
        sys.exit(1)

    compose = _docker_compose_cmd()
    if not compose:
        print("Docker Compose not found. Install Docker Desktop (includes compose).")
        sys.exit(1)


def _docker_compose_cmd() -> list[str] | None:
    if _run(["docker", "compose", "version"], check=False).returncode == 0:
        return ["docker", "compose"]
    if _which("docker-compose"):
        return ["docker-compose"]
    return None


def _copy_env_if_missing(src: Path, dest: Path) -> None:
    if not src.exists():
        print(f"  skip {dest.relative_to(ROOT)} (missing {src.relative_to(ROOT)})")
        return
    if dest.exists():
        print(f"  keep {dest.relative_to(ROOT)} (already exists)")
        return
    shutil.copy2(src, dest)
    print(f"  {src.relative_to(ROOT)} → {dest.relative_to(ROOT)}")


def _ensure_env_files() -> None:
    """Copy every .env.example to its runtime env file when the target is missing."""
    print("\n=== Environment files (.env.example → .env) ===")
    copies: list[tuple[Path, Path]] = [
        (ROOT / ".env.example", ROOT / ".env"),
        (BACKEND / ".env.example", BACKEND / ".env"),
        (CLIENT / ".env.example", CLIENT / ".env.local"),
    ]
    for src, dest in copies:
        _copy_env_if_missing(src, dest)


def _pull_postgres_image() -> None:
    print("\n=== PostgreSQL image ===")
    print(f"Compose uses pull_policy: never — ensuring {POSTGRES_IMAGE} is present locally.")
    _run(["docker", "pull", POSTGRES_IMAGE])


def _start_postgres() -> None:
    print("\n=== PostgreSQL (Docker) ===")
    compose = _docker_compose_cmd()
    assert compose is not None
    _run(compose + ["up", "-d"], cwd=ROOT)


def _wait_for_postgres(timeout_sec: int = 120) -> None:
    print("Waiting for PostgreSQL to accept connections...")
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        proc = subprocess.run(
            [
                "docker",
                "exec",
                POSTGRES_CONTAINER,
                "pg_isready",
                "-U",
                POSTGRES_USER,
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            print("PostgreSQL is ready.")
            return
        time.sleep(2)
    print("Timed out waiting for PostgreSQL. Check: docker compose logs postgres")
    sys.exit(1)


def _uv_sync(directory: Path, label: str) -> None:
    print(f"\n=== {label} (uv sync → .venv + dependencies) ===")
    if not (directory / "pyproject.toml").exists():
        print(f"  No pyproject.toml in {directory.relative_to(ROOT)} — skipped.")
        return
    _run(["uv", "sync"], cwd=directory)


def _migrate_and_seed(cse_demo: bool, skip_seed: bool) -> None:
    print("\n=== Database migrations ===")
    _run(["uv", "run", "alembic", "upgrade", "head"], cwd=BACKEND)

    if skip_seed:
        print("\n=== Seed skipped (--no-seed) ===")
        return

    print("\n=== Seed database ===")
    cmd = ["uv", "run", "python", "scripts/reseed.py"]
    if cse_demo:
        cmd.append("--cse-demo")
    _run(cmd, cwd=BACKEND)


def _client_install() -> None:
    print("\n=== Client (bun install) ===")
    _run(["bun", "install"], cwd=CLIENT)


def _popen_dev(cmd: list[str], cwd: Path) -> subprocess.Popen[bytes]:
    kwargs: dict = {
        "cwd": cwd,
        "env": os.environ.copy(),
    }
    if _is_windows():
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    return subprocess.Popen(cmd, **kwargs)


def _start_dev_servers() -> None:
    print("\n=== Dev servers ===")
    print("  API:    http://localhost:8000  (docs: /docs)")
    print("  Client: http://localhost:3000")
    print("  Login:  admin@demo.com / admin123  (role: Institution Admin)")
    print("\nPress Ctrl+C to stop both servers.\n")

    backend_proc = _popen_dev(
        ["uv", "run", "uvicorn", "app.main:app", "--reload", "--port", "8000"],
        BACKEND,
    )
    client_proc = _popen_dev(["bun", "run", "dev"], CLIENT)
    children = [backend_proc, client_proc]

    def _shutdown(*_args: object) -> None:
        for proc in children:
            if proc.poll() is None:
                if _is_windows():
                    proc.terminate()
                else:
                    os.killpg(proc.pid, signal.SIGTERM)

    if not _is_windows():
        signal.signal(signal.SIGINT, _shutdown)
        signal.signal(signal.SIGTERM, _shutdown)

    try:
        while True:
            for proc in children:
                if proc.poll() is not None:
                    raise RuntimeError(
                        f"Process exited early (code {proc.returncode}): {proc.args}"
                    )
            time.sleep(1)
    except KeyboardInterrupt:
        _shutdown()
    finally:
        for proc in children:
            if proc.poll() is None:
                proc.wait(timeout=10)


def _check_python_version() -> None:
    if sys.version_info < MIN_PYTHON:
        need = ".".join(map(str, MIN_PYTHON))
        have = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(f"This project needs Python {need}+ (backend/ML). Current: {have}.")
        print("Install Python 3.13+ from https://www.python.org/downloads/")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Set up ScholarPulse after git clone (macOS, Linux, Windows)."
    )
    parser.add_argument(
        "--start",
        action="store_true",
        help="After setup, run backend (uvicorn) and client (bun dev).",
    )
    parser.add_argument(
        "--no-docker",
        action="store_true",
        help="Skip Docker pull/compose (use if Postgres is already running).",
    )
    parser.add_argument(
        "--no-seed",
        action="store_true",
        help="Skip database reseed (migrations still run).",
    )
    parser.add_argument(
        "--cse-demo",
        action="store_true",
        help="Seed CSE/ECE/IST demo (~60 students/branch); default is bulk scale=100.",
    )
    parser.add_argument(
        "--skip-ml",
        action="store_true",
        help="Skip uv sync in ml/ (runtime only needs committed .pkl files).",
    )
    parser.add_argument(
        "--skip-client",
        action="store_true",
        help="Skip bun install (backend-only setup).",
    )
    args = parser.parse_args()

    print("ScholarPulse — automated setup")
    print(f"Root: {ROOT}")

    _check_python_version()
    _require_tools()
    _ensure_env_files()

    if not args.no_docker:
        _pull_postgres_image()
        _start_postgres()
        _wait_for_postgres()
    else:
        print("\n=== Docker skipped (--no-docker) ===")

    _uv_sync(BACKEND, "Backend")
    if not args.skip_ml:
        _uv_sync(ML, "ML")
    _migrate_and_seed(cse_demo=args.cse_demo, skip_seed=args.no_seed)

    if not args.skip_client:
        _client_install()

    print("\n=== Setup complete ===")
    if not args.start:
        print("Start manually:")
        print("  cd backend && uv run uvicorn app.main:app --reload --port 8000")
        print("  cd client && bun run dev")
        print("\nOr run:  python setup.py --start")
        return

    _start_dev_servers()


if __name__ == "__main__":
    main()
