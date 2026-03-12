import subprocess

from logger import get_logger

log = get_logger("brew.packages")


def _run(cmd: list[str], *, check: bool = True, dry_run: bool = False) -> subprocess.CompletedProcess | None:
    joined = " ".join(cmd)
    if dry_run:
        log.info("[DRY RUN] %s", joined)
        return None
    log.info("Running: %s", joined)
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def _brew() -> str:
    return "brew"


def install_formula(name: str, *, dry_run: bool = False) -> None:
    log.info("Installing formula: %s", name)
    _run([_brew(), "install", name], dry_run=dry_run)
    _run([_brew(), "upgrade", name], check=False, dry_run=dry_run)
    _run([_brew(), "unlink", name], check=False, dry_run=dry_run)
    _run([_brew(), "link", name], check=False, dry_run=dry_run)


def install_cask(name: str, *, dry_run: bool = False) -> None:
    log.info("Installing cask: %s", name)
    _run([_brew(), "install", "--cask", name], dry_run=dry_run)
    _run([_brew(), "upgrade", "--cask", name], check=False, dry_run=dry_run)


def install_formulae(formulae: list[str], *, dry_run: bool = False) -> None:
    for formula in formulae:
        install_formula(formula, dry_run=dry_run)


def install_casks(casks: list[str], *, dry_run: bool = False) -> None:
    for cask in casks:
        install_cask(cask, dry_run=dry_run)
