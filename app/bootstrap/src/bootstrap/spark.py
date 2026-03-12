import stat
from pathlib import Path

from logger import get_logger
from settings import get_brew_paths, get_platform
from shell import ZshrcEditor

log = get_logger("bootstrap.spark")

SECTION_HEADER = "Spark Path variables"
PYSPARK_SECTION_HEADER = "PySpark Path variables"


def _detect_spark_home() -> Path | None:
    """Auto-detect the latest installed Spark version in the Homebrew cellar."""
    paths = get_brew_paths(get_platform())
    spark_cellar = paths.cellar / "apache-spark"

    if not spark_cellar.exists():
        log.warning("apache-spark not found in %s", spark_cellar)
        return None

    versions = sorted(spark_cellar.iterdir(), reverse=True)
    if not versions:
        log.warning("No Spark versions found in %s", spark_cellar)
        return None

    latest = versions[0] / "libexec"
    log.info("Detected Spark home: %s", latest)
    return latest


def _make_bin_executable(spark_home: Path, *, dry_run: bool = False) -> None:
    bin_dir = spark_home / "bin"
    if not bin_dir.exists():
        return

    for script in bin_dir.iterdir():
        if script.is_file():
            if dry_run:
                log.info("[DRY RUN] Would chmod +x %s", script)
            else:
                script.chmod(script.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def configure_spark(editor: ZshrcEditor, *, dry_run: bool = False) -> None:
    spark_home = _detect_spark_home()
    if spark_home is None:
        log.warning("Skipping Spark configuration — not installed")
        return

    log.info("Configuring Spark environment")
    editor.remove_section(f"# {SECTION_HEADER}")
    editor.add_section(SECTION_HEADER, [
        f'export SPARK_HOME="{spark_home}"',
        'export PATH="$SPARK_HOME/bin/:$PATH"',
    ])

    _make_bin_executable(spark_home, dry_run=dry_run)


def configure_pyspark(editor: ZshrcEditor) -> None:
    log.info("Configuring PySpark environment")
    editor.remove_section(f"# {PYSPARK_SECTION_HEADER}")
    editor.add_section(PYSPARK_SECTION_HEADER, [
        'export PYSPARK_DRIVER_PYTHON=jupyter',
        "export PYSPARK_DRIVER_PYTHON_OPTS='notebook'",
    ])
