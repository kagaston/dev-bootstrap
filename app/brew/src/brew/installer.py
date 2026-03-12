import shutil
import subprocess

from logger import get_logger
from settings import get_brew_paths, get_platform

log = get_logger("brew.installer")


def _run(cmd: list[str], *, check: bool = True, dry_run: bool = False) -> subprocess.CompletedProcess | None:
    joined = " ".join(cmd)
    if dry_run:
        log.info("[DRY RUN] %s", joined)
        return None
    log.info("Running: %s", joined)
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def _brew_cmd() -> str:
    paths = get_brew_paths()
    exe = paths.brew_executable
    if exe.exists():
        return str(exe)
    return "brew"


def is_homebrew_installed() -> bool:
    return shutil.which("brew") is not None


def install_homebrew(*, dry_run: bool = False) -> None:
    if is_homebrew_installed():
        log.info("Homebrew is already installed")
        return

    log.info("Installing Homebrew...")
    install_script = "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
    _run(
        ["/bin/bash", "-c", f'$(curl -fsSL {install_script})'],
        dry_run=dry_run,
    )


def disable_analytics(*, dry_run: bool = False) -> None:
    log.info("Disabling Homebrew analytics")
    _run([_brew_cmd(), "analytics", "off"], dry_run=dry_run)


def update_homebrew(*, dry_run: bool = False) -> None:
    log.info("Updating Homebrew")
    _run([_brew_cmd(), "update", "--auto-update"], dry_run=dry_run)


def cleanup_homebrew(*, dry_run: bool = False) -> None:
    log.info("Cleaning up Homebrew")
    _run([_brew_cmd(), "cleanup", "--prune-prefix"], dry_run=dry_run)


def add_safe_directory(*, dry_run: bool = False) -> None:
    plat = get_platform()
    paths = get_brew_paths(plat)
    core_tap = paths.prefix / "Library" / "Taps" / "homebrew" / "homebrew-core"
    log.info("Adding Homebrew core to git safe directories")
    _run(
        ["git", "config", "--global", "--add", "safe.directory", str(core_tap)],
        dry_run=dry_run,
    )
