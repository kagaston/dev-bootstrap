import plistlib
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from logger import get_logger

log = get_logger("updater.scheduler")

LABEL = "com.dev-bootstrap.updater"
PLIST_DIR = Path.home() / "Library" / "LaunchAgents"
PLIST_PATH = PLIST_DIR / f"{LABEL}.plist"

_INTERVAL_PRESETS = {
    "hourly": 3600,
    "daily": 86400,
    "weekly": 604800,
}


@dataclass(frozen=True)
class ScheduleInfo:
    installed: bool
    label: str
    interval_seconds: int | None
    plist_path: Path
    dev_bootstrap_path: str | None


def _find_dev_bootstrap() -> str | None:
    return shutil.which("dev-bootstrap")


def _build_plist(interval_seconds: int, executable: str, log_dir: Path) -> dict:
    log_dir.mkdir(parents=True, exist_ok=True)
    return {
        "Label": LABEL,
        "ProgramArguments": [executable, "update"],
        "StartInterval": interval_seconds,
        "StandardOutPath": str(log_dir / "updater-stdout.log"),
        "StandardErrorPath": str(log_dir / "updater-stderr.log"),
        "RunAtLoad": False,
    }


def schedule_updates(
    interval: str = "weekly",
    *,
    interval_seconds: int | None = None,
    dry_run: bool = False,
) -> ScheduleInfo:
    """Install a macOS LaunchAgent that runs `dev-bootstrap update` on a schedule.

    Args:
        interval: One of "hourly", "daily", "weekly".
        interval_seconds: Override with an exact number of seconds.
        dry_run: Preview without writing anything.
    """
    seconds = interval_seconds or _INTERVAL_PRESETS.get(interval)
    if seconds is None:
        raise ValueError(f"Unknown interval '{interval}'. Use one of: {', '.join(_INTERVAL_PRESETS)}")

    executable = _find_dev_bootstrap()
    if executable is None:
        raise RuntimeError(
            "Cannot find 'dev-bootstrap' on PATH. "
            "Run 'uv sync' first so the CLI entry point is installed."
        )

    log_dir = Path.home() / "Library" / "Logs" / "dev-bootstrap"
    plist_data = _build_plist(seconds, executable, log_dir)

    if dry_run:
        log.info("[DRY RUN] Would write LaunchAgent plist to %s", PLIST_PATH)
        log.info("[DRY RUN] Interval: %d seconds (%s)", seconds, interval)
        log.info("[DRY RUN] Executable: %s", executable)
        log.info("[DRY RUN] Logs: %s", log_dir)
        return ScheduleInfo(
            installed=False,
            label=LABEL,
            interval_seconds=seconds,
            plist_path=PLIST_PATH,
            dev_bootstrap_path=executable,
        )

    unschedule_updates()

    PLIST_DIR.mkdir(parents=True, exist_ok=True)
    with open(PLIST_PATH, "wb") as f:
        plistlib.dump(plist_data, f)
    log.info("Wrote LaunchAgent plist to %s", PLIST_PATH)

    subprocess.run(["launchctl", "load", str(PLIST_PATH)], check=True)
    log.info("Loaded LaunchAgent '%s' (every %d seconds)", LABEL, seconds)

    return ScheduleInfo(
        installed=True,
        label=LABEL,
        interval_seconds=seconds,
        plist_path=PLIST_PATH,
        dev_bootstrap_path=executable,
    )


def unschedule_updates(*, dry_run: bool = False) -> bool:
    """Remove the LaunchAgent. Returns True if it was present."""
    if not PLIST_PATH.exists():
        log.info("No existing schedule found at %s", PLIST_PATH)
        return False

    if dry_run:
        log.info("[DRY RUN] Would unload and remove %s", PLIST_PATH)
        return True

    subprocess.run(["launchctl", "unload", str(PLIST_PATH)], check=False)
    PLIST_PATH.unlink()
    log.info("Removed LaunchAgent '%s'", LABEL)
    return True


def get_schedule_status() -> ScheduleInfo:
    """Check whether the auto-update schedule is currently installed."""
    if not PLIST_PATH.exists():
        return ScheduleInfo(
            installed=False,
            label=LABEL,
            interval_seconds=None,
            plist_path=PLIST_PATH,
            dev_bootstrap_path=_find_dev_bootstrap(),
        )

    with open(PLIST_PATH, "rb") as f:
        data = plistlib.load(f)

    return ScheduleInfo(
        installed=True,
        label=LABEL,
        interval_seconds=data.get("StartInterval"),
        plist_path=PLIST_PATH,
        dev_bootstrap_path=data.get("ProgramArguments", [None])[0],
    )
