import subprocess

from logger import get_logger
from shell import ZshrcEditor

log = get_logger("bootstrap.python")

SECTION_HEADER = "Python Aliases"


def configure_python(editor: ZshrcEditor, *, dry_run: bool = False) -> None:
    log.info("Configuring Python environment")

    if not dry_run:
        log.info("Upgrading pip")
        subprocess.run(
            ["python3", "-m", "pip", "install", "--upgrade", "pip"],
            check=False, capture_output=True, text=True,
        )
    else:
        log.info("[DRY RUN] Would upgrade pip")

    editor.remove_section(f"# {SECTION_HEADER}")
    editor.add_section(SECTION_HEADER, [
        'alias python="python3"',
        'alias pip="pip3"',
    ])
