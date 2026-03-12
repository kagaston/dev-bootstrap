from logger import get_logger
from settings import get_platform, Platform, FORMULAE, CASKS
from shell import ZshrcEditor
from brew import (
    install_homebrew,
    update_homebrew,
    cleanup_homebrew,
    disable_analytics,
    install_formulae,
    install_casks,
)
from brew.installer import add_safe_directory

from bootstrap.ruby import configure_ruby
from bootstrap.python import configure_python
from bootstrap.spark import configure_spark

log = get_logger("bootstrap.runner")


def _check_platform() -> bool:
    plat = get_platform()
    if plat in (Platform.MACOS_ARM, Platform.MACOS_INTEL):
        log.info("Detected platform: %s", plat.value)
        return True
    log.warning("Unsupported platform: %s — bootstrap is macOS only", plat.value)
    return False


def run_bootstrap(*, dry_run: bool = False) -> None:
    if not _check_platform():
        return

    editor = ZshrcEditor(dry_run=dry_run)
    editor.load()
    editor.backup()

    add_safe_directory(dry_run=dry_run)
    install_homebrew(dry_run=dry_run)
    disable_analytics(dry_run=dry_run)
    update_homebrew(dry_run=dry_run)

    install_formulae(FORMULAE, dry_run=dry_run)
    install_casks(CASKS, dry_run=dry_run)
    cleanup_homebrew(dry_run=dry_run)

    configure_ruby(editor)
    configure_python(editor, dry_run=dry_run)
    configure_spark(editor, dry_run=dry_run)

    editor.remove_blank_lines()
    editor.save()
    editor.reload_shell_hint()

    log.info("Bootstrap complete")


def check_bootstrap() -> None:
    log.info("Running bootstrap in dry-run mode (no changes will be made)")
    run_bootstrap(dry_run=True)
