import subprocess
from datetime import datetime

from logger import get_logger
from settings import FORMULAE, CASKS

log = get_logger("updater")


def _run(cmd: list[str], *, check: bool = True, dry_run: bool = False) -> subprocess.CompletedProcess | None:
    joined = " ".join(cmd)
    if dry_run:
        log.info("[DRY RUN] %s", joined)
        return None
    log.info("Running: %s", joined)
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def update_homebrew(*, dry_run: bool = False) -> None:
    log.info("Updating Homebrew itself")
    _run(["brew", "update", "--auto-update"], dry_run=dry_run)


def upgrade_formula(name: str, *, dry_run: bool = False) -> None:
    _run(["brew", "upgrade", name], check=False, dry_run=dry_run)


def upgrade_cask(name: str, *, dry_run: bool = False) -> None:
    _run(["brew", "upgrade", "--cask", name], check=False, dry_run=dry_run)


def cleanup(*, dry_run: bool = False) -> None:
    log.info("Cleaning up old versions")
    _run(["brew", "cleanup", "--prune-prefix"], dry_run=dry_run)


def run_update(*, dry_run: bool = False) -> None:
    """Update Homebrew and upgrade all managed formulae and casks."""
    start = datetime.now()
    log.info("Starting update at %s", start.strftime("%Y-%m-%d %H:%M:%S"))

    update_homebrew(dry_run=dry_run)

    log.info("Upgrading %d formulae", len(FORMULAE))
    for formula in FORMULAE:
        log.info("Upgrading formula: %s", formula)
        upgrade_formula(formula, dry_run=dry_run)

    log.info("Upgrading %d casks", len(CASKS))
    for cask in CASKS:
        log.info("Upgrading cask: %s", cask)
        upgrade_cask(cask, dry_run=dry_run)

    cleanup(dry_run=dry_run)

    elapsed = datetime.now() - start
    log.info("Update complete in %.1f seconds", elapsed.total_seconds())
